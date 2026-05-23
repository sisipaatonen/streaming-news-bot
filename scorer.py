"""AI-powered article scoring using Claude Haiku."""

import json
import os
import urllib.request

FENCE = chr(96) * 3


def call_claude(prompt, api_key):
    """Call Claude Haiku API."""
    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 3072,
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
    NL = chr(10)
    article_list = ""
    for i, a in enumerate(articles):
        desc = (a.get("description") or "")[:300]
        source = a.get("source", "")
        title = a.get("title", "")
        article_list += str(i) + ". [" + source + "] " + title + NL + "   " + desc + NL + NL

    prompt = (
        "You are a news relevance scorer for a daily digest. Score each article 1-10 "
        "against the user interests below. Be generous on borderline calls when an article "
        "plausibly fits the interest profile - this digest is meant to be a broad read - "
        "but DO penalize obvious off-topic (gadget reviews, deal pages, plot recaps, etc.)." + NL + NL +
        "For each article, return a score, a short factual summary, and a one-line note on why it fits (or doesn't)." + NL + NL +
        "USER INTERESTS:" + NL + interests + NL + NL +
        "SCORING GUIDE:" + NL +
        "- 9-10: Bullseye - directly on the highest-value topics in the interest profile." + NL +
        "- 7-8: Strong fit - clearly relevant, in the user's wheelhouse." + NL +
        "- 5-6: Reasonable - touches the area or is useful context even if not a perfect fit." + NL +
        "- 3-4: Tangential - mostly off-topic but mentions something relevant." + NL +
        "- 1-2: Not relevant (off-topic, listicle, recap, gadget review, generic deal)." + NL + NL +
        "Respond with ONLY a JSON object: {\"articles\": [...]}. Each element must have:" + NL +
        "- index: the article number (integer)" + NL +
        "- score: integer 1-10" + NL +
        "- summary: one-sentence factual summary of the article (max 25 words)" + NL +
        "- fit: one-sentence note on why this is or is not relevant (max 20 words)" + NL + NL +
        "ARTICLES TO SCORE:" + NL + article_list
    )
    return prompt


def _in_range(idx, length):
    return idx != -1 and idx in range(length)


def score_articles_ai(articles, interest_profile):
    """Score articles with Claude. Mutates each article with ai_score, ai_summary, ai_fit."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("  No ANTHROPIC_API_KEY set, skipping AI scoring")
        return articles

    print(f"    Scoring {len(articles)} articles with Claude Haiku")

    batch_size = 8
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        prompt = build_scoring_prompt(batch, interest_profile)
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
            if isinstance(result, list):
                scored = result
            else:
                scored = result.get("articles", result if isinstance(result, list) else [])
            for item in scored:
                idx = item.get("index", -1)
                if _in_range(idx, len(batch)):
                    batch[idx]["ai_score"] = item.get("score", 5)
                    batch[idx]["ai_summary"] = item.get("summary", "")
                    batch[idx]["ai_fit"] = item.get("fit", item.get("reason", ""))
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"    Failed to parse AI scores: {e}")

    for a in articles:
        if "ai_score" not in a:
            a["ai_score"] = 5
            a["ai_summary"] = ""
            a["ai_fit"] = "Not scored"

    articles.sort(key=lambda x: x.get("ai_score", 0), reverse=True)
    return articles
