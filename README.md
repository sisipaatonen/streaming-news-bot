# Streaming News Bot

Daily email digest for myStaze. Focus: the live streaming & broadcasting industry —
platforms (Twitch, Kick, YouTube Live, TikTok Live, DAZN, ESPN+, Fight Pass),
broadcast rights deals, live streaming tech, live sports distribution, live music
and performing arts streaming. Combat sports is a preferred vertical *for the
streaming/rights angle* — not fight cards or rankings.

## Philosophy

Cast a wide net across general tech, business, media, and industry publications
rather than chasing niche streaming-only sources. A refined weighted keyword
algorithm surfaces live-streaming-relevant articles wherever they appear, and
Claude Haiku then scores each survivor, writes a short summary, and explains why
it fits. No categories — just one ranked list.

Pipeline per run:
1. Fetch every source in `FEEDS` (general tech, media, sports business, music,
   community signals).
2. Drop articles older than 48h, dedupe by title, drop URLs already seen.
3. Keyword pre-filter: each article gets a score from `STREAMING_KEYWORDS` (with
   negative penalties from `NEGATIVE_KEYWORDS`). Articles below
   `keyword_threshold` are dropped; the top `ai_score_limit` go to AI.
4. Claude Haiku scores 1-10, writes a one-line summary and a "why it fits" note.
5. Top `digest_limit` stories at or above `ai_min_score` are emailed.

Tune the gates in `feeds.py` → `DIGEST_CONFIG["streaming"]`.

## Setup

### Environment variables (set in Railway dashboard)
- `GMAIL_USER` — Gmail address to send from
- `GMAIL_TOKEN_B64` — base64-encoded Gmail OAuth pickle (see `startup.py`)
- `ANTHROPIC_API_KEY` — Claude API key for scoring
- `SEND_TIME_STREAMING` — Override default send time (UTC), default `06:00`
- `RUN_ON_START` — Set to `true` to send immediately on deploy (for testing)
- `RUN_TOPIC` — When `RUN_ON_START=true`, restrict to one topic (e.g. `streaming`)

### Railway Deploy
1. Push this repo to GitHub
2. Connect to Railway
3. Add environment variables
4. Deploy

## Recipients
See `feeds.py` → `DIGEST_CONFIG["streaming"]["recipients"]`.

## Sources
General tech (TechCrunch, The Verge, Ars Technica, Wired, Engadget, VentureBeat,
Mashable, TechRadar, ZDNet, 9to5Mac, 9to5Google, Hacker News, MIT Tech Review),
media/business (Digiday, Adweek, Fast Company, Axios), TV/film (Variety,
Deadline, Hollywood Reporter), streaming trade (StreamTV Insider, TV Tech, Next
TV, Light Reading), sports business (SportsPro Media, Front Office Sports,
Sportico), music industry (Music Business Worldwide, Pollstar, Music Ally,
Billboard Biz), and community signals (Reddit cordcutters/Twitch/LivestreamFail).
