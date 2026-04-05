"""Unified news bot - streaming + tech digests with AI scoring."""

import json
import os
import re
import sqlite3
import urllib.request
import urllib.parse
import base64
import pickle
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from xml.etree import ElementTree as ET

from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from feeds import FEEDS, DIGEST_CONFIG
from scorer import score_articles_ai


GMAIL_USER = os.environ.get("GMAIL_USER", "pasi.siitonen@gmail.com")
GMAIL_TOKEN_PATH = os.environ.get("GMAIL_TOKEN_PATH", "/app/gmail_token.pickle")
DB_PATH = os.environ.get("DB_PATH", "/app/news.db")


# --- Database ---

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE IF NOT EXISTS seen_articles (
            url_hash TEXT PRIMARY KEY,
            title TEXT,
            first_seen TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    return db


def is_seen(db, url):
    url_hash = str(hash(url))
    row = db.execute("SELECT 1 FROM seen_articles WHERE url_hash = ?", (url_hash,)).fetchone()
    return row is not None


def mark_seen(db, url, title):
    url_hash = str(hash(url))
    db.execute("INSERT OR IGNORE INTO seen_articles (url_hash, title) VALUES (?, ?)", (url_hash, title))
    db.commit()


def cleanup_old(db, days=14):
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    db.execute("DELETE FROM seen_articles WHERE first_seen is not null and first_seen not in (select first_seen from seen_articles order by first_seen desc limit 5000)")
    db.commit()


# --- Gmail ---

def _get_gmail_service():
    creds = None
    if os.path.exists(GMAIL_TOKEN_PATH):
        with open(GMAIL_TOKEN_PATH, "rb") as f:
            creds = pickle.load(f)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(GMAIL_TOKEN_PATH, "wb") as f:
            pickle.dump(creds, f)
    if not creds or not creds.valid:
        raise Exception(f"Gmail token invalid or missing at {GMAIL_TOKEN_PATH}")
    return build("gmail", "v1", credentials=creds)


def send_email(html, subject, recipients):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText("Open in HTML-capable email client.", "plain"))
    msg.attach(MIMEText(html, "html"))

    service = _get_gmail_service()
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"  Email sent to {len(recipients)} recipients")


# --- Feed Fetching ---


def _is_recent(pub_dt, cutoff):
    if pub_dt is None:
        return True
    # Return True if article is newer than cutoff
    diff = pub_dt.timestamp() - cutoff.timestamp()
    return diff == abs(diff)

def fetch_feed(feed):
    try:
        req = urllib.request.Request(
            feed["url"],
            headers={"User-Agent": "NewsBot/2.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  Failed {feed.get("name")}: {e}")
        return None


def parse_feed(xml_content, feed):
    articles = []
    try:
        root = ET.fromstring(xml_content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items = root.findall(".//item") or root.findall(".//atom:entry", ns) or root.findall(".//entry")

        for item in items[:20]:
            def get(tag, attr=None):
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
                link_el = item.find("link")
                if link_el is not None:
                    link = link_el.get("href", "") or link_el.text or ""
            description = get("description") or get("summary") or get("content")
            pub_date = get("pubDate") or get("published") or get("updated")

            # Strip HTML
            description = re.sub(r"" + chr(60) + "[^" + chr(62) + "]+" + chr(62), " ", description or "")
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
                except (ValueError, AttributeError):
                    continue

            if title and link:
                articles.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "pub_dt": pub_dt,
                    "source": feed["name"],
                    "category": feed["category"],
                    "topics": feed.get("topics", []),
                })
    except ET.ParseError as e:
        print(f"  XML parse error: {e}")
    return articles


def fetch_all_articles(topic):
    all_articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)

    topic_feeds = [f for f in FEEDS if topic in f.get("topics", [])]
    print(f"  Fetching {len(topic_feeds)} feeds for topic: {topic}")

    for feed in topic_feeds:
        print(f"    {feed.get("name")}...")
        xml = fetch_feed(feed)
        if not xml:
            continue
        articles = parse_feed(xml, feed)
        for a in articles:
            if _is_recent(a.get("pub_dt"), cutoff):
                all_articles.append(a)

    # Deduplicate by title
    seen_titles = set()
    unique = []
    for a in all_articles:
        key = re.sub(r"[^a-z0-9]", "", a["title"].lower())[:40]
        if key not in seen_titles:
            seen_titles.add(key)
            unique.append(a)

    return unique


def build_html(articles, topic):
    config = DIGEST_CONFIG[topic]
    today = datetime.now().strftime("%A, %B %d %Y")
    LT = chr(60)
    GT = chr(62)
    NL = chr(10)

    by_category = {}
    for a in articles[:40]:
        cat = a["category"]
        by_category.setdefault(cat, []).append(a)

    sections_html = ""
    for cat in config["category_order"]:
        items = by_category.get(cat, [])
        if not items:
            continue
        label = config["category_labels"].get(cat, cat.title())
        items_html = ""
        for a in items[:10]:
            ai = a.get("ai_score", 0)
            fire = chr(128293) if ai not in range(0, 8) else chr(11088) if ai not in range(0, 6) else ""
            pub_str = ""
            if a["pub_dt"]:
                pub_str = a["pub_dt"].strftime("%b %d, %H:%M UTC")
            reason = a.get("ai_reason", "")
            score_badge = ""
            if ai and ai != 5:
                score_badge = f" [{ai}/10]"
            items_html += (
                LT + "div class=" + chr(34) + "article" + chr(34) + GT + NL +
                LT + "div class=" + chr(34) + "article-meta" + chr(34) + GT + NL +
                LT + "span class=" + chr(34) + "source" + chr(34) + GT + a["source"] + LT + "/span" + GT + NL +
                LT + "span class=" + chr(34) + "date" + chr(34) + GT + pub_str + LT + "/span" + GT + NL +
                (LT + "span class=" + chr(34) + "hot" + chr(34) + GT + fire + LT + "/span" + GT + NL if fire else "") +
                LT + "/div" + GT + NL +
                LT + "a href=" + chr(34) + a["link"] + chr(34) + " class=" + chr(34) + "article-title" + chr(34) + GT + a["title"] + score_badge + LT + "/a" + GT + NL +
                (LT + "p class=" + chr(34) + "article-desc" + chr(34) + GT + reason + LT + "/p" + GT + NL if reason else "") +
                LT + "/div" + GT + NL
            )
        sections_html += (
            LT + "div class=" + chr(34) + "section" + chr(34) + GT + NL +
            LT + "div class=" + chr(34) + "section-title" + chr(34) + GT + label + LT + "/div" + GT + NL +
            items_html +
            LT + "/div" + GT + NL
        )

    return _html_wrapper(today, config, sections_html, len(articles))


def _html_wrapper(today, config, sections_html, article_count):
    LT = chr(60)
    GT = chr(62)
    NL = chr(10)
    Q = chr(34)
    SC = chr(59)
    title = config["emoji"] + " " + config["title"]
    css = _get_css(SC, NL)
    html = (
        LT + "!DOCTYPE html" + GT + NL +
        LT + "html" + GT + NL +
        LT + "head" + GT + NL +
        LT + "meta charset=" + Q + "UTF-8" + Q + GT + NL +
        LT + "title" + GT + title + " - " + today + LT + "/title" + GT + NL +
        LT + "style" + GT + css + LT + "/style" + GT + NL +
        LT + "/head" + GT + NL +
        LT + "body" + GT + NL +
        LT + "div class=" + Q + "header" + Q + GT + NL +
        LT + "h1" + GT + title + LT + "/h1" + GT + NL +
        LT + "div class=" + Q + "date" + Q + GT + today + LT + "/div" + GT + NL +
        LT + "span class=" + Q + "badge" + Q + GT + str(article_count) + " articles - AI-scored" + LT + "/span" + GT + NL +
        LT + "/div" + GT + NL +
        LT + "div class=" + Q + "content" + Q + GT + NL +
        sections_html +
        LT + "/div" + GT + NL +
        LT + "div class=" + Q + "footer" + Q + GT + "Powered by Nexus AI" + LT + "/div" + GT + NL +
        LT + "/body" + GT + NL +
        LT + "/html" + GT
    )
    return html


def _get_css(SC, NL):
    s = SC
    rules = [
        "body { font-family: Segoe UI, Arial, sans-serif" + s + " background: #0f0f13" + s + " color: #e0e0f0" + s + " margin: 0" + s + " padding: 0" + s + " }",
        ".header { background: linear-gradient(135deg, #1a0a3d, #0a2a2a)" + s + " padding: 40px 32px" + s + " text-align: center" + s + " border-bottom: 2px solid #2e2e42" + s + " }",
        ".header h1 { margin: 0" + s + " font-size: 28px" + s + " }",
        ".header .date { color: #8888aa" + s + " margin-top: 8px" + s + " font-size: 14px" + s + " }",
        ".badge { display: inline-block" + s + " background: rgba(124,109,250,0.2)" + s + " border: 1px solid rgba(124,109,250,0.4)" + s + " color: #7c6dfa" + s + " padding: 4px 14px" + s + " border-radius: 20px" + s + " font-size: 12px" + s + " margin-top: 12px" + s + " }",
        ".content { max-width: 700px" + s + " margin: 0 auto" + s + " padding: 24px 16px" + s + " }",
        ".section { margin-bottom: 36px" + s + " }",
        ".section-title { font-size: 16px" + s + " font-weight: 700" + s + " text-transform: uppercase" + s + " color: #4fd1c5" + s + " border-bottom: 1px solid #2e2e42" + s + " padding-bottom: 10px" + s + " margin-bottom: 16px" + s + " }",
        ".article { background: #1a1a24" + s + " border: 1px solid #2e2e42" + s + " border-radius: 10px" + s + " padding: 16px 18px" + s + " margin-bottom: 12px" + s + " }",
        ".article-meta { display: flex" + s + " align-items: center" + s + " gap: 10px" + s + " margin-bottom: 8px" + s + " }",
        ".source { font-size: 11px" + s + " font-weight: 700" + s + " text-transform: uppercase" + s + " color: #7c6dfa" + s + " }",
        ".date { font-size: 11px" + s + " color: #8888aa" + s + " }",
        ".article-title { color: #e8e8f0" + s + " font-size: 15px" + s + " font-weight: 600" + s + " text-decoration: none" + s + " display: block" + s + " }",
        ".article-desc { margin: 8px 0 0" + s + " font-size: 13px" + s + " color: #9999bb" + s + " }",
        ".footer { text-align: center" + s + " padding: 24px" + s + " color: #8888aa" + s + " font-size: 12px" + s + " border-top: 1px solid #2e2e42" + s + " }",
    ]
    return NL.join(rules)


def run_digest(topic):
    config = DIGEST_CONFIG[topic]
    divider = chr(61) * 50
    print(divider)
    print(f"Running {topic} digest...")
    print(divider)

    articles = fetch_all_articles(topic)
    print(f"  Got {len(articles)} unique articles")

    if not articles:
        print("  No articles found, skipping.")
        return

    db = get_db()
    new_articles = []
    for a in articles:
        if not is_seen(db, a["link"]):
            new_articles.append(a)
            mark_seen(db, a["link"], a["title"])
    db.close()

    print(f"  {len(new_articles)} new articles (after dedup)")
    if not new_articles:
        print("  All articles already sent, skipping.")
        return

    scored = score_articles_ai(new_articles, topic)

    html = build_html(scored, topic)
    today = datetime.now().strftime("%B %d, %Y")
    emoji = config.get("emoji", "")
    digest_title = config.get("title", topic)
    subject = emoji + " " + digest_title + " - " + today + " (" + str(len(scored)) + " stories)"
    send_email(html, subject, config["recipients"])
    print(f"  Done! Sent to {len(config.get("recipients", []))} recipients")


def run():
    """Run all digests."""
    for topic in DIGEST_CONFIG:
        run_digest(topic)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        run_digest(sys.argv[1])
    else:
        run()
