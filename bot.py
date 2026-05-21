"""News bot - live streaming digest with keyword pre-filter + AI scoring."""

import base64
import json
import os
import pickle
import re
import sqlite3
import traceback
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from xml.etree import ElementTree as ET

from feeds import FEEDS, DIGEST_CONFIG, STREAMING_KEYWORDS, NEGATIVE_KEYWORDS, TITLE_BLOCKLIST
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


# --- Gmail API (HTTPS, no SMTP needed) ---

def _get_gmail_credentials():
    """Load and refresh Gmail OAuth credentials."""
    if not os.path.exists(GMAIL_TOKEN_PATH):
        raise Exception(f"Gmail token not found at {GMAIL_TOKEN_PATH}")
    with open(GMAIL_TOKEN_PATH, "rb") as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        data = urllib.parse.urlencode({
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "refresh_token": creds.refresh_token,
            "grant_type": "refresh_token"
        }).encode()
        req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_data = json.loads(resp.read())
        creds.token = token_data["access_token"]
        with open(GMAIL_TOKEN_PATH, "wb") as f:
            pickle.dump(creds, f)
    if not creds.token:
        raise Exception("Gmail token has no access_token and could not refresh")
    return creds


def send_email(html, subject, recipients):
    creds = _get_gmail_credentials()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText("Open in HTML-capable email client.", "plain"))
    msg.attach(MIMEText(html, "html"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    body = json.dumps({"raw": raw}).encode()
    req = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=body, method="POST",
        headers={
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    print(f"  Email sent to {len(recipients)} recipients")


# --- Feed Fetching ---


def _is_recent(pub_dt, cutoff):
    if pub_dt is None:
        return True
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
        print(f"  Failed {feed.get('name')}: {e}")
        return None


def parse_feed(xml_content, feed):
    articles = []
    try:
        root = ET.fromstring(xml_content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items = root.findall(".//item") or root.findall(".//atom:entry", ns) or root.findall(".//entry")

        for item in items[:25]:
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

            description = re.sub(r"" + chr(60) + "[^" + chr(62) + "]+" + chr(62), " ", description or "")
            description = re.sub(r"\s+", " ", description).strip()[:400]

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
                })
    except ET.ParseError as e:
        print(f"  XML parse error: {e}")
    return articles


def fetch_all_articles():
    all_articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)

    print(f"  Fetching {len(FEEDS)} feeds")

    for feed in FEEDS:
        print(f"    {feed.get('name')}...")
        xml = fetch_feed(feed)
        if not xml:
            continue
        articles = parse_feed(xml, feed)
        for a in articles:
            if _is_recent(a.get("pub_dt"), cutoff):
                all_articles.append(a)

    seen_titles = set()
    unique = []
    for a in all_articles:
        key = re.sub(r"[^a-z0-9]", "", a["title"].lower())[:40]
        if key not in seen_titles:
            seen_titles.add(key)
            unique.append(a)

    return unique


# --- Keyword pre-filter ---


def compute_keyword_score(article):
    """Score article 0+ on streaming relevance via weighted keywords.

    Title matches count double. Negative keywords subtract 8 each. Returns
    (score, matched_keywords).
    """
    title = (article.get("title") or "").lower()
    desc = (article.get("description") or "").lower()
    haystack = " " + title + " " + desc + " "
    title_pad = " " + title + " "

    score = 0
    matched = []
    for weight, keywords in STREAMING_KEYWORDS.items():
        for kw in keywords:
            in_title = kw in title_pad
            in_desc = (not in_title) and (kw in haystack)
            if in_title:
                score += weight * 2
                matched.append(kw)
            elif in_desc:
                score += weight
                matched.append(kw)

    for neg in NEGATIVE_KEYWORDS:
        if neg in haystack:
            score -= 8

    return score, matched


def is_title_blocked(article):
    """True if the headline matches any TITLE_BLOCKLIST combo (all tokens present)."""
    title = (article.get("title") or "").lower()
    for combo in TITLE_BLOCKLIST:
        if all(token in title for token in combo):
            return True
    return False


def keyword_prefilter(articles, threshold, limit):
    """Annotate articles with keyword_score, drop below threshold, keep top `limit`."""
    blocked = 0
    for a in articles:
        if is_title_blocked(a):
            a["keyword_score"] = -1000
            a["keyword_matches"] = ["BLOCKED: title pattern"]
            blocked += 1
            continue
        s, m = compute_keyword_score(a)
        a["keyword_score"] = s
        a["keyword_matches"] = m
    if blocked:
        print(f"  {blocked} articles hard-blocked by title pattern")

    survivors = [a for a in articles if a["keyword_score"] >= threshold]
    survivors.sort(key=lambda x: x["keyword_score"], reverse=True)
    return survivors[:limit]


# --- HTML rendering ---


def build_html(articles, config):
    today = datetime.now().strftime("%A, %B %d %Y")
    LT = chr(60)
    GT = chr(62)
    NL = chr(10)
    Q = chr(34)

    items_html = ""
    for a in articles:
        ai = a.get("ai_score", 0)
        if ai >= 8:
            fire = chr(128293)
        elif ai >= 6:
            fire = chr(11088)
        else:
            fire = ""
        pub_str = ""
        if a.get("pub_dt"):
            pub_str = a["pub_dt"].strftime("%b %d, %H:%M UTC")
        summary = a.get("ai_summary", "") or ""
        fit = a.get("ai_fit", "") or ""
        score_badge = f" [{ai}/10]" if ai else ""
        items_html += (
            LT + "div class=" + Q + "article" + Q + GT + NL +
            LT + "div class=" + Q + "article-meta" + Q + GT + NL +
            LT + "span class=" + Q + "source" + Q + GT + a["source"] + LT + "/span" + GT + NL +
            LT + "span class=" + Q + "date" + Q + GT + pub_str + LT + "/span" + GT + NL +
            (LT + "span class=" + Q + "hot" + Q + GT + fire + LT + "/span" + GT + NL if fire else "") +
            LT + "/div" + GT + NL +
            LT + "a href=" + Q + a["link"] + Q + " class=" + Q + "article-title" + Q + GT + a["title"] + score_badge + LT + "/a" + GT + NL +
            (LT + "p class=" + Q + "article-summary" + Q + GT + summary + LT + "/p" + GT + NL if summary else "") +
            (LT + "p class=" + Q + "article-fit" + Q + GT + LT + "strong" + GT + "Why it fits: " + LT + "/strong" + GT + fit + LT + "/p" + GT + NL if fit else "") +
            LT + "/div" + GT + NL
        )

    return _html_wrapper(today, config, items_html, len(articles))


def _html_wrapper(today, config, items_html, article_count):
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
        LT + "span class=" + Q + "badge" + Q + GT + str(article_count) + " stories - keyword-filtered, AI-scored" + LT + "/span" + GT + NL +
        LT + "/div" + GT + NL +
        LT + "div class=" + Q + "content" + Q + GT + NL +
        items_html +
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
        ".content { max-width: 720px" + s + " margin: 0 auto" + s + " padding: 24px 16px" + s + " }",
        ".article { background: #1a1a24" + s + " border: 1px solid #2e2e42" + s + " border-radius: 10px" + s + " padding: 16px 18px" + s + " margin-bottom: 12px" + s + " }",
        ".article-meta { display: flex" + s + " align-items: center" + s + " gap: 10px" + s + " margin-bottom: 8px" + s + " }",
        ".source { font-size: 11px" + s + " font-weight: 700" + s + " text-transform: uppercase" + s + " color: #7c6dfa" + s + " }",
        ".date { font-size: 11px" + s + " color: #8888aa" + s + " }",
        ".article-title { color: #e8e8f0" + s + " font-size: 15px" + s + " font-weight: 600" + s + " text-decoration: none" + s + " display: block" + s + " }",
        ".article-summary { margin: 8px 0 0" + s + " font-size: 13px" + s + " color: #c8c8dd" + s + " line-height: 1.45" + s + " }",
        ".article-fit { margin: 6px 0 0" + s + " font-size: 12px" + s + " color: #9999bb" + s + " font-style: italic" + s + " }",
        ".article-fit strong { color: #4fd1c5" + s + " font-style: normal" + s + " }",
        ".footer { text-align: center" + s + " padding: 24px" + s + " color: #8888aa" + s + " font-size: 12px" + s + " border-top: 1px solid #2e2e42" + s + " }",
    ]
    return NL.join(rules)


def run_digest(topic):
    config = DIGEST_CONFIG[topic]
    divider = chr(61) * 50
    print(divider)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Running {topic} digest...")
    print(divider)

    try:
        articles = fetch_all_articles()
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

        threshold = config.get("keyword_threshold", 4)
        ai_limit = config.get("ai_score_limit", 80)
        candidates = keyword_prefilter(new_articles, threshold, ai_limit)
        print(f"  {len(candidates)} candidates after keyword filter (threshold={threshold})")
        if not candidates:
            print("  No candidates passed keyword filter, skipping.")
            return

        scored = score_articles_ai(candidates)

        hist = {}
        for a in scored:
            hist[a.get("ai_score", 0)] = hist.get(a.get("ai_score", 0), 0) + 1
        print(f"  AI score histogram: {dict(sorted(hist.items(), reverse=True))}")

        ai_min = config.get("ai_min_score", 4)
        digest_limit = config.get("digest_limit", 40)
        final = [a for a in scored if a.get("ai_score", 0) >= ai_min][:digest_limit]
        print(f"  {len(final)} stories in final digest (ai_min={ai_min})")
        if not final:
            print("  No stories passed AI score floor, skipping.")
            return

        html = build_html(final, config)
        today = datetime.now().strftime("%B %d, %Y")
        emoji = config.get("emoji", "")
        digest_title = config.get("title", topic)
        subject = emoji + " " + digest_title + " - " + today + " (" + str(len(final)) + " stories)"
        send_email(html, subject, config["recipients"])
        print(f"  Done! Sent to {len(config['recipients'])} recipients")
    except Exception as e:
        print(f"  ERROR in {topic} digest: {e}")
        traceback.print_exc()


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
