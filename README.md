# Streaming News Bot

Daily email digest for myStaze. Focus: the live streaming & broadcasting industry —
platforms (YouTube Live, Twitch, Kick, ESPN+, DAZN, Fight Pass), broadcast rights
deals, live streaming tech, live sports distribution, live music and performing
arts streaming. Combat sports is a preferred vertical *for the streaming/rights
angle* — not fight cards or rankings.

## Setup

### Environment variables (set in Railway dashboard)
- `GMAIL_USER` — Gmail address to send from
- `GMAIL_APP_PASSWORD` — Gmail App Password (not your regular password)
- `SEND_TIME` — Time to send daily digest, default `08:00` (UTC — Railway runs UTC)
- `RUN_ON_START` — Set to `true` to send immediately on deploy (for testing)

### Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Create a new app password for "Mail"
3. Paste it as GMAIL_APP_PASSWORD in Railway

### Railway Deploy
1. Push this repo to GitHub
2. Connect to Railway
3. Add environment variables
4. Deploy

## Recipients
- pasi.siitonen@gmail.com
- olli.karikoski@mystaze.com
- joonas.palkonen@mystaze.com

## Feeds
- Live streaming platforms & tech: StreamTV Insider, Next TV, TV Tech, The Verge
- Sports streaming & broadcasting: SportsPro Media, Awful Announcing
- TV/film streaming (context): Variety, Deadline, Hollywood Reporter
- Live music & performing arts: Pollstar, Music Business Worldwide, Music Ally
