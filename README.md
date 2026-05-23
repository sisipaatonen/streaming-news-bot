# Streaming & Tech News Bot

Daily email digest for myStaze. Two sections per email:

1. **Live Streaming & Broadcasting** — platforms (Twitch, Kick, YouTube Live,
   TikTok Live, DAZN, ESPN+, Fight Pass), broadcast/streaming rights deals,
   live streaming tech, live sports distribution, live music and performing
   arts streaming. Combat sports is a preferred vertical *for the
   streaming/rights angle* — not fight cards or rankings.
2. **Hot Tech for Startups** — cutting-edge tech a founder/CTO would want to
   stay sharp on: frontier AI models, agentic systems, dev tooling, startup
   funding rounds in deep tech, novel hardware, platform shifts.

## Philosophy

Per-category source sets and keyword filters. The streaming category casts a
wide net across general tech / media / sports business / music / community
sources with tight streaming-specific keywords. The tech category uses a small
curated set of high-signal tech publications with looser keywords, letting the
AI ranker do most of the work. Hard headline blocklist drops clickbait like
"how to watch X" outright in both sections.

Pipeline per run:
1. Fetch every source in `FEEDS` (union across categories).
2. Drop articles older than 48h, drop URLs already seen, drop cross-source
   near-duplicates via token-overlap Jaccard on the headline.
3. For each category, in declared order:
   - Restrict to that category's sources.
   - Apply `TITLE_BLOCKLIST` (hard drop).
   - Keyword-score with the category's keyword dict + negative keywords.
     Drop below `keyword_threshold`; pass the top `ai_score_limit` to AI.
   - Claude Haiku scores 1-10 against the category's interest profile,
     writes a one-line summary and a "why it fits" note.
   - Keep top `digest_limit` at or above `ai_min_score`.
   - Articles routed to this section are skipped in later sections.
4. Render the multi-section email and send via Gmail API.

Tune the gates per category in `feeds.py` →
`DIGEST_CONFIG["streaming"]["categories"]`.

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

**Tech category (curated, signal-rich):** TechCrunch, The Verge, Ars Technica,
Wired, VentureBeat, Hacker News, MIT Tech Review, The Information, IEEE Spectrum.

**Streaming category (broad net):** all of the above, plus Engadget, Mashable,
TechRadar, ZDNet, 9to5Mac, 9to5Google, Digiday, Adweek, Fast Company, Axios,
Variety, Deadline, Hollywood Reporter, StreamTV Insider, TV Tech, Next TV,
Light Reading, SportsPro Media, Front Office Sports, Sportico, Music Business
Worldwide, Pollstar, Music Ally, Billboard Biz, and Reddit r/cordcutters,
r/Twitch, r/LivestreamFail.
