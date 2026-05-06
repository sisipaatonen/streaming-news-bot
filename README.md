# Streaming News Bot

Daily email digest for myStaze. Primary focus: combat sports streaming (MMA, UFC, boxing) and the
live streaming landscape (platforms, tech, rights deals). Music streaming is included as a
deprioritized future-focus area.

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
- Combat sports: MMA Fighting, MMA Junkie, Sherdog, Bloody Elbow, BoxingScene
- Live streaming platforms & tech: Next TV, TV Tech, StreamTV Insider, The Verge, Ars Technica, VentureBeat
- Sports streaming business: SportsPro Media
- Entertainment streaming: Variety, Deadline, Hollywood Reporter
- Music streaming (future focus): Music Business Worldwide, Music Ally
