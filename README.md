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
Global coverage across the live-streaming umbrella: platforms & broadcast tech,
sports rights, creator/Twitch/esports, gambling, live music, TV/film.

- **Platforms & broadcast tech (global):** StreamTV Insider, Next TV, TV Tech,
  The Verge, Digital TV Europe, Broadband TV News, Advanced Television,
  Rapid TV News, TBI Vision, IBC365, Mumbrella (APAC)
- **Sports streaming & broadcasting (international):** SportsPro Media,
  SportBusiness, Inside the Games, World Soccer Talk, Sport Industry Group,
  Front Office Sports, Awful Announcing
- **Twitch / creators / esports / short-form:** Tubefilter, Dexerto,
  Esports Insider, The Esports Advocate, Social Media Today, Digiday
- **Gambling & sports betting:** SBC News, iGaming Business,
  Legal Sports Report, Gambling Insider
- **Live music & performing arts:** Pollstar, Music Business Worldwide,
  Music Ally, IQ Magazine, Hypebot
- **TV/film streaming (context):** Variety, Deadline, Hollywood Reporter,
  Screen Daily, Broadcast Now (UK)
