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
  `DIGEST_CONFIG` entry. Use `RUN_ON_START=true` (and optionally `RUN_TOPIC`)
  to fire immediately on deploy for testing.
- `bot.py` — fetches feeds, dedups against SQLite `seen_articles`, runs the
  keyword pre-filter, calls AI scoring, builds HTML, sends via Gmail API.
- `scorer.py` — Claude Haiku scoring; returns `ai_score`, `ai_summary`,
  `ai_fit` per article.
- `feeds.py` — `FEEDS` (wide source list), `STREAMING_KEYWORDS` (weighted),
  `NEGATIVE_KEYWORDS`, `INTEREST_PROFILE`, `DIGEST_CONFIG`.

## Filter philosophy

Cast a wide net across general tech/media/business feeds. Don't add niche
streaming-only sources just because they "fit." The weighted keyword filter
(title matches doubled, negative penalties) is the primary instrument for
finding relevant articles; the AI is the final ranker and writes the
summary + "why it fits" note. No categories — one flat ranked list.

Tune behaviour via `DIGEST_CONFIG["streaming"]`:
`keyword_threshold`, `ai_score_limit`, `ai_min_score`, `digest_limit`.

## Things to avoid

- Don't push only to a feature branch and expect it to deploy.
- Don't reintroduce per-category sections in the email — the user wants a
  single ranked list.
- Don't add sources like Awful Announcing that flood the digest with
  fight-card / recap noise. Sports business sources should be
  rights/distribution-focused (SportsPro, Front Office Sports, Sportico).
