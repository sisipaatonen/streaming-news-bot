# CLAUDE.md

Notes for Claude / coding agents working on this repo.

## Deployment

**Railway deploys from `master`.** Always merge work into `master` and push
`master` for changes to actually go live. Pushing only a feature branch does
nothing — Railway will keep running whatever's on `master`.

The standard flow:

1. Do work on the assigned feature branch (e.g. `claude/<task>`).
2. Commit and push the feature branch.
3. Fast-forward `master` to the feature branch, then `git push origin master`.
4. Railway picks up the change on `master` and redeploys the worker.

No PRs are needed — the user merges directly to `master`.

## Architecture

- `main.py` — long-running worker; schedules `run_digest` daily per
  top-level `DIGEST_CONFIG` entry. Use `RUN_ON_START=true` (and optionally
  `RUN_TOPIC`) to fire immediately on deploy for testing.
- `bot.py` — fetches feeds, dedups (URL via SQLite `seen_articles` +
  cross-source Jaccard on significant title tokens), then processes each
  category in `DIGEST_CONFIG[topic]["categories"]` independently with its
  own sources / keywords / interest profile / thresholds. Builds a
  multi-section HTML email and sends via Gmail API.
- `scorer.py` — Claude Haiku scoring; takes an `interest_profile`
  parameter so each category scores against its own profile. Returns
  `ai_score`, `ai_summary`, `ai_fit` per article.
- `feeds.py` — feed lists, per-category keyword dictionaries, interest
  profiles, hard `TITLE_BLOCKLIST`, and `DIGEST_CONFIG` with a
  `categories` list per digest.

## Categories

The digest has two sections, declared in
`DIGEST_CONFIG["streaming"]["categories"]` and processed in order:

1. **streaming** — broad source set (`STREAMING_SOURCES`: general tech +
   media + sports business + music + community), tight streaming-specific
   keywords (`STREAMING_KEYWORDS` / `STREAMING_NEGATIVE_KEYWORDS`),
   `STREAMING_INTEREST_PROFILE`.
2. **tech** — small vetted source set (`TECH_SOURCES`: just the
   signal-rich general-tech publications), looser tech/startup keywords
   (`TECH_KEYWORDS` / `TECH_NEGATIVE_KEYWORDS`), `TECH_INTEREST_PROFILE`.

Articles assigned to an earlier category never reappear in a later one
within the same run.

## Filter philosophy

For **streaming**: cast a wide net across publications, rely on tight
weighted keywords (title matches doubled, negative penalties) to surface
the live-streaming/broadcasting angle. AI is the final ranker.

For **tech**: keep the source list curated and small. Keywords are loose
(low `keyword_threshold`) because the sources themselves are already
filtered for signal. AI does most of the ranking.

`TITLE_BLOCKLIST` is a hard pre-filter applied to BOTH categories — every
tuple is a set of substrings that, if ALL present in the lowercased
title, drops the article outright. Use it for clickbait patterns
("how to watch", "watch ... for free") that no scoring tweak can save.

Tune per-category via the section's own keys:
`keyword_threshold`, `ai_score_limit`, `ai_min_score`, `digest_limit`.

## Things to avoid

- Don't push only to a feature branch and expect it to deploy.
- Don't add sources like Awful Announcing that flood the digest with
  fight-card / recap noise. Sports business sources should be
  rights/distribution-focused (SportsPro, Front Office Sports, Sportico).
- Don't put gadget-review / leak-heavy pubs (Engadget, TechRadar, ZDNet,
  9to5*, Mashable) into `TECH_SOURCES` — they live in streaming-only on
  purpose; the tech category is for cutting-edge / startup-relevant
  signal, not consumer commerce.
