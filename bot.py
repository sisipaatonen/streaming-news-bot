import os
import re
import json
import smtplib
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xml.etree import ElementTree as ET

from feeds import FEEDS, KEYWORDS_HIGH, KEYWORDS_MEDIUM

RECIPIENTS = [
    "pasi.siitonen@gmail.com",
    "olli.karikoski@mystaze.com",
    "joonas.palkonen@mystaze.com",
]

GMAIL_USER = os.environ.get("GMAIL_USER", "pasi.siitonen@gmail.com")
GMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD", "")


def fetch_feed(feed):
    try:
        req = urllib.request.Request(
            feed["url"],
            headers={"User-Agent": "StreamingNewsBot/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  ❌ {feed['name']}: {e}")
        return None


def parse_feed(xml_content, feed):
    articles = []
    try:
        root = ET.fromstring(xml_content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # Handle both RSS and Atom
        items = root.findall(".//item") or root.findall(".//atom:entry", ns) or root.findall(".//entry")

        for item in items[:20]:
            def get(tag, attr=None):
                # Try with and without namespace
                for t in [tag, f"atom:{tag}"]:
                    el = item.find(t, ns)
                    if el is None:
                        el = item.find(tag)
                    if el is not None:
                        if attr:
                            return el.get(attr, "")
                        return (el.text or "").strip()
                return ""

            title = get("title")
            link = get("link")
            if not link:
                # Atom uses link href
                link_el = item.find("link")
                if link_el is not None:
                    link = link_el.get("href", "") or link_el.text or ""
            description = get("description") or get("summary") or get("content")
            pub_date = get("pubDate") or get("published") or get("updated")

            # Strip HTML from description
            description = re.sub(r"<[^>]+>", " ", description or "")
            description = re.sub(r"\s+", " ", description).strip()[:300]

            # Parse date
            pub_dt = None
            for fmt in [
                "%a, %d %b %Y %H:%M:%S %z",
                "%a, %d %b %Y %H:%M:%S GMT",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d",
            ]:
                try:
                    pub_dt = datetime.strptime(pub_date.strip(), fmt)
                    if pub_dt.tzinfo is None:
                        pub_dt = pub_dt.replace(tzinfo=timezone.utc)
                    break
                except:
                    continue

            if title and link:
                articles.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "source": feed["name"],
                    "category": feed["category"],
                    "pub_dt": pub_dt,
                })
    except Exception as e:
        print(f"  ⚠️  Parse error for {feed['name']}: {e}")
    return articles


def score_article(article):
    text = (article["title"] + " " + article["description"]).lower()
    score = 0

    for kw in KEYWORDS_HIGH:
        if kw in text:
            score += 10

    for kw in KEYWORDS_MEDIUM:
        if kw in text:
            score += 3

    # Recency bonus
    if article["pub_dt"]:
        age_hours = (datetime.now(timezone.utc) - article["pub_dt"]).total_seconds() / 3600
        if age_hours < 12:
            score += 15
        elif age_hours < 24:
            score += 8
        elif age_hours < 48:
            score += 3

    # Category bonus
    if article["category"] in ("music", "streaming"):
        score += 5

    article["score"] = score
    return article


def fetch_all_articles():
    all_articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)

    for feed in FEEDS:
        print(f"  Fetching {feed['name']}...")
        xml = fetch_feed(feed)
        if not xml:
            continue
        articles = parse_feed(xml, feed)
        for a in articles:
            # Filter to last 48h only if we have a date
            if a["pub_dt"] and a["pub_dt"] < cutoff:
                continue
            score_article(a)
            all_articles.append(a)

    # Deduplicate by title similarity
    seen_titles = set()
    unique = []
    for a in all_articles:
        key = re.sub(r"[^a-z0-9]", "", a["title"].lower())[:40]
        if key not in seen_titles:
            seen_titles.add(key)
            unique.append(a)

    # Sort by score desc
    unique.sort(key=lambda x: x["score"], reverse=True)
    return unique


CATEGORY_LABELS = {
    "music": "🎵 Music Streaming",
    "streaming": "📺 Streaming Platforms & Tech",
    "tech": "💻 Tech",
    "sports": "⚽ Sports Streaming",
    "entertainment": "🎬 Entertainment",
}


def build_html(articles):
    today = datetime.now().strftime("%A, %B %d %Y")

    # Group by category
    by_category = {}
    for a in articles[:40]:  # max 40 articles
        cat = a["category"]
        by_category.setdefault(cat, []).append(a)

    # Build sections
    sections_html = ""
    for cat in ["music", "streaming", "sports", "entertainment", "tech"]:
        items = by_category.get(cat, [])
        if not items:
            continue
        label = CATEGORY_LABELS.get(cat, cat.title())
        items_html = ""
        for a in items[:10]:
            score_bar = "🔥" if a["score"] >= 30 else "⭐" if a["score"] >= 15 else ""
            pub_str = ""
            if a["pub_dt"]:
                pub_str = a["pub_dt"].strftime("%b %d, %H:%M UTC")
            items_html += f"""
            <div class="article">
              <div class="article-meta">
                <span class="source">{a['source']}</span>
                <span class="date">{pub_str}</span>
                {f'<span class="hot">{score_bar}</span>' if score_bar else ''}
              </div>
              <a class="article-title" href="{a['link']}" target="_blank">{a['title']}</a>
              {f'<p class="article-desc">{a["description"][:200]}...</p>' if a["description"] else ''}
            </div>"""

        sections_html += f"""
        <div class="section">
          <h2 class="section-title">{label}</h2>
          {items_html}
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Streaming News Daily — {today}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f0f13; color: #e0e0f0; margin: 0; padding: 0; }}
  .header {{ background: linear-gradient(135deg, #1a0a3d, #0a2a2a); padding: 40px 32px; text-align: center; border-bottom: 2px solid #2e2e42; }}
  .header h1 {{ margin: 0; font-size: 28px; letter-spacing: -0.5px; }}
  .header .date {{ color: #8888aa; margin-top: 8px; font-size: 14px; }}
  .badge {{ display: inline-block; background: rgba(124,109,250,0.2); border: 1px solid rgba(124,109,250,0.4); color: #7c6dfa; padding: 4px 14px; border-radius: 20px; font-size: 12px; margin-top: 12px; }}
  .content {{ max-width: 700px; margin: 0 auto; padding: 24px 16px; }}
  .section {{ margin-bottom: 36px; }}
  .section-title {{ font-size: 16px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #4fd1c5; border-bottom: 1px solid #2e2e42; padding-bottom: 10px; margin-bottom: 16px; }}
  .article {{ background: #1a1a24; border: 1px solid #2e2e42; border-radius: 10px; padding: 16px 18px; margin-bottom: 12px; }}
  .article-meta {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }}
  .source {{ font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #7c6dfa; }}
  .date {{ font-size: 11px; color: #8888aa; }}
  .hot {{ font-size: 13px; }}
  .article-title {{ color: #e8e8f0; font-size: 15px; font-weight: 600; text-decoration: none; line-height: 1.4; display: block; }}
  .article-title:hover {{ color: #4fd1c5; }}
  .article-desc {{ margin: 8px 0 0; font-size: 13px; color: #9999bb; line-height: 1.5; }}
  .footer {{ text-align: center; padding: 24px; color: #8888aa; font-size: 12px; border-top: 1px solid #2e2e42; }}
</style>
</head>
<body>
<div class="header">
  <h1>📡 Streaming News Daily</h1>
  <div class="date">{today}</div>
  <div class="badge">{len(articles)} stories scored & ranked</div>
</div>
<div class="content">
{sections_html}
</div>
<div class="footer">
  Streaming News Bot · myStaze Music · Powered by Nexus<br>
  🔥 = Top story &nbsp;⭐ = Recommended
</div>
</body>
</html>"""


def send_email(html, article_count):
    today = datetime.now().strftime("%B %d, %Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📡 Streaming News Daily — {today} ({article_count} stories)"
    msg["From"] = GMAIL_USER
    msg["To"] = ", ".join(RECIPIENTS)

    text_part = MIMEText(f"Streaming News Daily {today}\nOpen in HTML-capable email client for best experience.", "plain")
    html_part = MIMEText(html, "html")
    msg.attach(text_part)
    msg.attach(html_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, RECIPIENTS, msg.as_string())

    print(f"✅ Email sent to {len(RECIPIENTS)} recipients")


def run():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching streaming news...")
    articles = fetch_all_articles()
    print(f"  Got {len(articles)} unique scored articles")

    html = build_html(articles)
    send_email(html, len(articles))
    print("Done.")


if __name__ == "__main__":
    run()
