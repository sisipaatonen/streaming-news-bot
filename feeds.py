FEEDS = [
    # Live streaming platforms, tech, and trade press
    {"name": "StreamTV Insider", "url": "https://www.streamtvinsider.com/rss/all", "category": "streaming", "topics": ["streaming"]},
    {"name": "Next TV", "url": "https://www.nexttv.com/rss.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "TV Tech", "url": "https://www.tvtechnology.com/rss.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "category": "streaming", "topics": ["streaming"]},

    # Sports streaming & broadcasting (rights, platforms, distribution - NOT match results)
    {"name": "SportsPro Media", "url": "https://www.sportspromedia.com/feed/", "category": "sports", "topics": ["streaming"]},
    {"name": "Awful Announcing", "url": "https://awfulannouncing.com/feed", "category": "sports", "topics": ["streaming"]},

    # TV/film streaming (context for the broader live distribution landscape)
    {"name": "Variety", "url": "https://variety.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Deadline", "url": "https://deadline.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/feed/", "category": "entertainment", "topics": ["streaming"]},

    # Live music & performing arts streaming
    {"name": "Pollstar", "url": "https://www.pollstar.com/feed/", "category": "music", "topics": ["streaming"]},
    {"name": "Music Business Worldwide", "url": "https://www.musicbusinessworldwide.com/feed/", "category": "music", "topics": ["streaming"]},
    {"name": "Music Ally", "url": "https://musically.com/feed/", "category": "music", "topics": ["streaming"]},
]


# Interest profiles for AI scoring per topic
INTEREST_PROFILES = {
    "streaming": """We are myStaze, a live streaming platform. Our interest is the LIVE STREAMING and BROADCASTING industry - how live content is distributed, monetized, and consumed.

HIGH-VALUE TOPICS (score 8-10):
- Live streaming platforms: YouTube Live, Twitch, Kick, ESPN+, DAZN, UFC Fight Pass, NBA League Pass, MLB.tv, Disney+ live events, Amazon Prime Video live, Paramount+ live, Netflix live, Triller, FloSports, Stage+, Boiler Room, Veeps. Platform launches, feature changes, monetization changes, exits, M&A.
- Broadcast and streaming RIGHTS DEALS: who wins what, fees, exclusivity, geographic splits, length of deal, sub-licensing.
- Live streaming TECHNOLOGY: low-latency protocols (LL-HLS, WebRTC, CMAF), encoding, transcoding, CDN, DRM, server-side ad insertion, multi-angle, interactive features, AI in live production, captions/translation.
- Live SPORTS broadcasting and streaming distribution across NFL, NBA, MLB, NHL, EPL, UEFA, F1, UFC, boxing PPVs, ONE Championship, PFL, etc.
- Live MUSIC streaming: concerts, festivals, DJ sets and shows on Twitch/YouTube, paid livestream concerts, virtual concerts, livestream tours.
- Live PERFORMING ARTS streaming: theatre, opera, comedy specials, livestreamed events.
- Creator economy as it touches live streaming.

PREFERRED VERTICAL: combat sports (UFC, MMA, boxing, kickboxing) - but ONLY when the article is about broadcasting, streaming, rights, platforms, distribution, or business. Score these high when relevant.

DO NOT SCORE HIGH (score 1-3):
- Fight cards, fight previews, fighter rankings, tournament/event results, fighter signings/releases, drug tests, retirements, injury updates, weigh-ins.
- Match recaps, team standings, transfer news, player stats, game previews with no broadcasting/distribution angle.
- On-demand recorded music streaming (Spotify, Apple Music, Tidal product/business news) UNLESS it is about live audio, concerts, or live distribution.
- TV/film streaming product news (Netflix subscriber numbers, show cancellations, on-demand catalogue moves) UNLESS it intersects with live distribution or sports rights.

A useful test: would this article help us understand how live content is distributed, priced, or technically delivered? If yes, score high. If it is about who fought whom, who won, or what someone released on Spotify, score low.""",
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
        "category_order": ["streaming", "sports", "entertainment", "music"],
        "category_labels": {
            "streaming": "📺 Live Streaming Platforms & Tech",
            "sports": "🏆 Sports Streaming & Broadcasting",
            "entertainment": "🎬 TV & Film Streaming",
            "music": "🎵 Live Music & Performing Arts",
        },
    },
}
