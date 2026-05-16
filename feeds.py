FEEDS = [
    # ---------------------------------------------------------------------
    # Live streaming platforms, broadcast tech & trade press (global)
    # ---------------------------------------------------------------------
    {"name": "StreamTV Insider", "url": "https://www.streamtvinsider.com/rss/all", "category": "streaming", "topics": ["streaming"]},
    {"name": "Next TV", "url": "https://www.nexttv.com/rss.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "TV Tech", "url": "https://www.tvtechnology.com/rss.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "Digital TV Europe", "url": "https://www.digitaltveurope.com/feed/", "category": "streaming", "topics": ["streaming"]},
    {"name": "Broadband TV News", "url": "https://www.broadbandtvnews.com/feed/", "category": "streaming", "topics": ["streaming"]},
    {"name": "Advanced Television", "url": "https://advanced-television.com/feed/", "category": "streaming", "topics": ["streaming"]},
    {"name": "Rapid TV News", "url": "https://www.rapidtvnews.com/index.php?format=feed&type=rss", "category": "streaming", "topics": ["streaming"]},
    {"name": "TBI Vision", "url": "https://tbivision.com/feed/", "category": "streaming", "topics": ["streaming"]},
    {"name": "IBC365", "url": "https://www.ibc.org/rss/all-news.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "Mumbrella (APAC)", "url": "https://mumbrella.com.au/feed", "category": "streaming", "topics": ["streaming"]},

    # ---------------------------------------------------------------------
    # Sports streaming & broadcasting (rights, platforms, distribution)
    # International coverage - football/soccer, cricket, rugby, F1, etc.
    # ---------------------------------------------------------------------
    {"name": "SportsPro Media", "url": "https://www.sportspromedia.com/feed/", "category": "sports", "topics": ["streaming"]},
    {"name": "SportBusiness", "url": "https://www.sportbusiness.com/feed/", "category": "sports", "topics": ["streaming"]},
    {"name": "Inside the Games", "url": "https://www.insidethegames.biz/rss", "category": "sports", "topics": ["streaming"]},
    {"name": "World Soccer Talk", "url": "https://worldsoccertalk.com/feed/", "category": "sports", "topics": ["streaming"]},
    {"name": "Sport Industry Group", "url": "https://www.sportindustry.biz/feed/", "category": "sports", "topics": ["streaming"]},
    {"name": "Awful Announcing", "url": "https://awfulannouncing.com/feed", "category": "sports", "topics": ["streaming"]},
    {"name": "Front Office Sports", "url": "https://frontofficesports.com/feed/", "category": "sports", "topics": ["streaming"]},

    # ---------------------------------------------------------------------
    # Creator economy, Twitch / Kick / YouTube, esports, short-form video
    # ---------------------------------------------------------------------
    {"name": "Tubefilter", "url": "https://www.tubefilter.com/feed/", "category": "creators", "topics": ["streaming"]},
    {"name": "Dexerto", "url": "https://www.dexerto.com/feed/", "category": "creators", "topics": ["streaming"]},
    {"name": "Esports Insider", "url": "https://esportsinsider.com/feed", "category": "creators", "topics": ["streaming"]},
    {"name": "The Esports Advocate", "url": "https://esportsadvocate.net/feed/", "category": "creators", "topics": ["streaming"]},
    {"name": "Social Media Today", "url": "https://www.socialmediatoday.com/feeds/news/", "category": "creators", "topics": ["streaming"]},
    {"name": "Digiday", "url": "https://digiday.com/feed/", "category": "creators", "topics": ["streaming"]},

    # ---------------------------------------------------------------------
    # Gambling & sports betting (intersects with live sports streaming)
    # ---------------------------------------------------------------------
    {"name": "SBC News", "url": "https://sbcnews.co.uk/feed/", "category": "gambling", "topics": ["streaming"]},
    {"name": "iGaming Business", "url": "https://igamingbusiness.com/feed/", "category": "gambling", "topics": ["streaming"]},
    {"name": "Legal Sports Report", "url": "https://www.legalsportsreport.com/feed/", "category": "gambling", "topics": ["streaming"]},
    {"name": "Gambling Insider", "url": "https://www.gamblinginsider.com/rss/news.php", "category": "gambling", "topics": ["streaming"]},

    # ---------------------------------------------------------------------
    # Live music & performing arts streaming (international)
    # ---------------------------------------------------------------------
    {"name": "Pollstar", "url": "https://www.pollstar.com/feed/", "category": "music", "topics": ["streaming"]},
    {"name": "Music Business Worldwide", "url": "https://www.musicbusinessworldwide.com/feed/", "category": "music", "topics": ["streaming"]},
    {"name": "Music Ally", "url": "https://musically.com/feed/", "category": "music", "topics": ["streaming"]},
    {"name": "IQ Magazine", "url": "https://www.iq-mag.net/feed/", "category": "music", "topics": ["streaming"]},
    {"name": "Hypebot", "url": "https://www.hypebot.com/hypebot/atom.xml", "category": "music", "topics": ["streaming"]},

    # ---------------------------------------------------------------------
    # TV/film streaming (context for the broader live distribution landscape)
    # ---------------------------------------------------------------------
    {"name": "Variety", "url": "https://variety.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Deadline", "url": "https://deadline.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Screen Daily", "url": "https://www.screendaily.com/Rss/News", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Broadcast Now (UK)", "url": "https://www.broadcastnow.co.uk/Rss/all-news", "category": "entertainment", "topics": ["streaming"]},
]


# Interest profiles for AI scoring per topic
INTEREST_PROFILES = {
    "streaming": """We are myStaze, a live streaming platform. Our interest is the GLOBAL LIVE STREAMING and BROADCASTING industry - how live content is distributed, monetized, and consumed across every vertical, on every continent. Live streaming is the umbrella; it covers live sports, live music, esports, creator livestreams, gambling-integrated live content, short-form video, and live TV.

We want a GLOBAL view, not a US/NFL-centric one. International leagues, non-US platforms, and stories from Europe, Latin America, Asia, Africa and Oceania are explicitly welcome.

HIGH-VALUE TOPICS (score 8-10):
- Live streaming PLATFORMS: Twitch, Kick, YouTube Live / YouTube Gaming, Rumble, TikTok Live, Instagram Live, Facebook Live / Facebook Gaming, X (Twitter) live video, DLive, Trovo, AfreecaTV, Bigo Live, Nimo TV, Huya, Douyu, NicoNico Douga, BIGO. Platform launches, feature changes, monetization changes, exclusivity deals, creator deals, bans/exits, M&A, layoffs.
- Sports streaming SERVICES: ESPN+, DAZN, UFC Fight Pass, NBA League Pass, MLB.tv, NFL+, MLS Season Pass, Apple TV+ sports, Amazon Prime Video sports, Peacock sports, FuboTV, Sky Sports / Sky Glass / NOW, TNT Sports (UK), Discovery+ / Eurosport, Viaplay, beIN Sports, Stan Sport, Kayo, Optus Sport, JioCinema / JioHotstar, SonyLIV, FanCode, Willow, ESPN Star, Setanta, ELEVEN Sports, OneFootball, LaLigaTV, Premier Sports.
- Broadcast and streaming RIGHTS DEALS: who wins what (Premier League, La Liga, Bundesliga, Serie A, Ligue 1, UEFA Champions League / Europa, AFC, CAF, CONMEBOL Libertadores, Copa America, Euros, World Cup, Olympics, IPL / cricket, NFL, NBA, MLB, NHL, F1, MotoGP, UFC, boxing PPVs, tennis Slams, golf majors, rugby, AFL, NRL, Super Rugby, J-League, K-League, MLS, Liga MX). Fees, exclusivity, geographic splits, sub-licensing, FAST channel launches.
- Live streaming TECHNOLOGY: low-latency protocols (LL-HLS, WebRTC, CMAF, SRT, RIST), encoding, transcoding, CDN, DRM, server-side ad insertion, multi-angle, interactive features, AI in live production, real-time captions/translation, cloud production, REMI/at-home production.
- ESPORTS broadcasting and streaming: LoL Worlds, CS / Valorant majors, Dota Internationals, Mobile Legends, PUBG, Fortnite events, esports rights deals, league streaming exclusivity.
- CREATOR ECONOMY and INFLUENCER live streaming: top streamers (Kai Cenat, IShowSpeed, xQc, Pokimane, Adin Ross, Asmongold, Sapnap, etc.), streamer moves between platforms, exclusive deals, subathons, creator awards, IRL streaming.
- Live MUSIC streaming: concerts, festivals, DJ sets and live shows on Twitch/YouTube, paid livestream concerts, virtual concerts, livestream tours, Boiler Room, Cercle, Veeps, Stage+, Mandolin, Sessions Live.
- Live PERFORMING ARTS streaming: theatre, opera, comedy specials, livestreamed events.
- GAMBLING & SPORTS BETTING as it integrates with live streaming: in-stream betting, micro-betting, live odds overlays, streamer-gambling controversies (slots streaming, sponsorships), regulatory action affecting live-stream betting, sportsbook streaming rights.
- SHORT-FORM VIDEO as it touches live: TikTok Live, YouTube Shorts live integrations, Instagram Live, Snapchat live, short-form-to-live monetization.

PREFERRED VERTICAL: combat sports (UFC, MMA, boxing, kickboxing, ONE Championship, PFL, Bellator legacy, Karate Combat, Glory) - but ONLY when the article is about broadcasting, streaming, rights, platforms, distribution, or business. Score these high when relevant.

DO NOT SCORE HIGH (score 1-3):
- Match results, fight cards, fight previews, fighter rankings, tournament/event results, fighter signings/releases, drug tests, retirements, injury updates, weigh-ins, team standings, transfers, player stats, game previews - UNLESS there is a clear broadcasting/distribution/rights angle.
- On-demand recorded music streaming (Spotify, Apple Music, Tidal product/business news) UNLESS it is about live audio, concerts, or live distribution.
- TV/film streaming product news (Netflix subscriber numbers, show cancellations, on-demand catalogue moves) UNLESS it intersects with live distribution, live events, sports rights, or platform competition for live audiences.
- Pure gambling product news (new slot launches, casino bonuses, poker tournaments) UNLESS it ties into live streaming, in-stream betting, or sports broadcast integration.
- US-centric trivia that does not generalise (e.g. a small US local sports radio change with no national or international distribution relevance).

A useful test: would this article help us understand how live content is distributed, priced, technically delivered, or monetised - anywhere in the world? If yes, score high. If it is about who won, who signed where, or what someone released on Spotify, score low.""",
}


# Digest configuration per topic
DIGEST_CONFIG = {
    "streaming": {
        "title": "Live Streaming & Broadcasting Daily",
        "emoji": "📡",
        "recipients": [
            "pasi.siitonen@gmail.com",
            "olli.karikoski@mystaze.com",
            "joonas.palkonen@mystaze.com",
            "bjorn.masalin@gmail.com",
            "sarah@wavelength.now",
            "al@extremeinternational.com",
        ],
        "send_time": "06:00",
        "category_order": ["streaming", "sports", "creators", "gambling", "music", "entertainment"],
        "category_labels": {
            "streaming": "📺 Live Streaming Platforms & Tech",
            "sports": "🏆 Sports Streaming & Broadcasting",
            "creators": "🎮 Twitch, Creators & Esports",
            "gambling": "🎰 Gambling & Sports Betting",
            "music": "🎵 Live Music & Performing Arts",
            "entertainment": "🎬 TV & Film Streaming",
        },
    },
}
