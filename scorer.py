"""AI-powered article scoring using Claude Haiku."""

import json
import os
import urllib.request

from feeds import INTEREST_PROFILES

LT = chr(60)
GT = chr(62)
FENCE = chr(96) * 3


def call_claude(prompt, api_key):
    """Call Claude Haiku API."""
    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"]
    except Exception as e:
        print(f"    Claude API error: {e}")
        return None


def build_scoring_prompt(articles, interests):
    article_list = ""
    for i, a in enumerate(articles):
        desc = (a.get("description") or "")[:200]
        source = a.get("source", "")
        title = a.get("title", "")
        article_list += str(i) + ". [" + source + "] " + title + chr(10) + "   " + desc + chr(10) + chr(10)

    prompt = "You are a news relevance scorer. Score each article for relevance to the user interests." + chr(10) + chr(10)
    prompt += "USER INTERESTS:" + chr(10) + interests + chr(10) + chr(10)
    prompt += "SCORING GUIDE:" + chr(10)
    prompt += "- 9-10: Directly about the user core projects/tools" + chr(10)
    prompt += "- 7-8: Strongly related technology or business area" + chr(10)
    prompt += "- 4-6: Tangentially related" + chr(10)
    prompt += "- 1-3: Not relevant" + chr(10) + chr(10)
    prompt += "Respond with ONLY a JSON object. Each element must have:" + chr(10)
    prompt += "- index: the article number" + chr(10)
    prompt += "- score: integer 1-10" + chr(10)
    prompt += "- reason: brief explanation" + chr(10) + chr(10)
    prompt += "ARTICLES TO SCORE:" + chr(10) + article_list
    return prompt


def _in_range(idx, length):
    return idx != -1 and idx in range(length)


def score_articles_ai(articles, topic):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("  No ANTHROPIC_API_KEY set, skipping AI scoring")
        return articles

    interests = INTEREST_PROFILES.get(topic, "")
    if not interests:
        print(f"  No interest profile for topic: {topic}")
        return articles

    print(f"  Scoring {len(articles)} articles with Claude Haiku for topic: {topic}")

    batch_size = 8
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        prompt = build_scoring_prompt(batch, interests)
        raw = call_claude(prompt, api_key)

        if not raw:
            print(f"    Skipping batch {i // batch_size + 1} (API unavailable)")
            continue

        try:
            text = raw.strip()
            if text.startswith(FENCE):
                text = text.split(chr(10), 1)[1]
                text = text.rsplit(FENCE, 1)[0]
            result = json.loads(text)
            scored = result.get("articles", [])
            for item in scored:
                idx = item.get("index", -1)
                if _in_range(idx, len(batch)):
                    batch[idx]["ai_score"] = item.get("score", 5)
                    batch[idx]["ai_reason"] = item.get("reason", "")
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"    Failed to parse AI scores: {e}")

    for a in articles:
        if "ai_score" not in a:
            a["ai_score"] = 5
            a["ai_reason"] = "Not scored"

    articles.sort(key=lambda x: x.get("ai_score", 0), reverse=True)
    return articles
