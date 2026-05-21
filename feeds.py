"""News sources, keyword filter, and interest profile.

Philosophy: cast a wide net across general tech, business, media, and industry
publications. Don't try to find perfectly-fitting streaming-only sources. Instead,
rely on a refined weighted keyword algorithm to surface live-streaming-relevant
articles wherever they appear, then AI-score the survivors.
"""

FEEDS = [
    # General tech press (broadest coverage of platforms, products, deals, tech)
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"},
    {"name": "Wired", "url": "https://www.wired.com/feed/rss"},
    {"name": "Engadget", "url": "https://www.engadget.com/rss.xml"},
    {"name": "VentureBeat", "url": "https://venturebeat.com/feed/"},
    {"name": "Mashable", "url": "https://mashable.com/feeds/rss/all"},
    {"name": "TechRadar", "url": "https://www.techradar.com/rss"},
    {"name": "ZDNet", "url": "https://www.zdnet.com/news/rss.xml"},
    {"name": "9to5Mac", "url": "https://9to5mac.com/feed/"},
    {"name": "9to5Google", "url": "https://9to5google.com/feed/"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage"},
    {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
    {"name": "The Information (free)", "url": "https://www.theinformation.com/feed"},

    # Media, marketing & the business of attention
    {"name": "Digiday", "url": "https://digiday.com/feed/"},
    {"name": "Adweek", "url": "https://www.adweek.com/feed/"},
    {"name": "Fast Company", "url": "https://www.fastcompany.com/latest/rss"},
    {"name": "Axios", "url": "https://api.axios.com/feed/"},

    # TV / film industry trade
    {"name": "Variety", "url": "https://variety.com/feed/"},
    {"name": "Deadline", "url": "https://deadline.com/feed/"},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/feed/"},

    # Streaming / video industry trade
    {"name": "StreamTV Insider", "url": "https://www.streamtvinsider.com/rss/all"},
    {"name": "TV Tech", "url": "https://www.tvtechnology.com/rss.xml"},
    {"name": "Next TV", "url": "https://www.nexttv.com/rss.xml"},
    {"name": "Light Reading", "url": "https://www.lightreading.com/rss_simple.asp"},

    # Sports business (rights, distribution, deals — not match recaps)
    {"name": "SportsPro Media", "url": "https://www.sportspromedia.com/feed/"},
    {"name": "Front Office Sports", "url": "https://frontofficesports.com/feed/"},
    {"name": "Sportico", "url": "https://www.sportico.com/feed/"},

    # Music industry
    {"name": "Music Business Worldwide", "url": "https://www.musicbusinessworldwide.com/feed/"},
    {"name": "Pollstar", "url": "https://www.pollstar.com/feed/"},
    {"name": "Music Ally", "url": "https://musically.com/feed/"},
    {"name": "Billboard Biz", "url": "https://www.billboard.com/c/business/feed/"},

    # Community signals
    {"name": "Reddit: cordcutters", "url": "https://www.reddit.com/r/cordcutters/.rss"},
    {"name": "Reddit: Twitch", "url": "https://www.reddit.com/r/Twitch/.rss"},
    {"name": "Reddit: livestreamfail", "url": "https://www.reddit.com/r/LivestreamFail/.rss"},
]


# Weighted keyword dictionary. Title matches count double in scoring.
# Higher weight = stronger signal that the article is about live streaming
# or broadcasting in a way we care about.
STREAMING_KEYWORDS = {
    # Definitive signals — almost always relevant
    10: [
        "live stream", "livestream", "live streaming", "live-stream", "livestreaming",
        "broadcast rights", "streaming rights", "media rights deal", "tv rights deal",
        "low-latency", "low latency video", "ll-hls", "webrtc",
        "server-side ad insertion", "ssai", "dynamic ad insertion",
        "fast channel", "ott platform", "ott service",
        "pay-per-view", "pay per view", " ppv ",
        "live broadcast", "live coverage", "live event streaming",
        "linear channel", "linear streaming",
    ],
    # Streaming platforms / services — strong signal
    8: [
        "twitch", "kick.com", "kick streamer", "kick.com streamer",
        "youtube live", "youtube tv", "youtube creator",
        "tiktok live", "instagram live", "facebook live", "x live",
        "dazn", "espn+", "espn plus", "fight pass", "ufc fight pass",
        "mlb.tv", "nba league pass", "nfl+", "nfl plus", "nhl.tv",
        "fubotv", "fubo tv", "sling tv", "hulu live",
        "veeps", "moment house", "stage+", "stageplus",
        "trovo", "rumble", "dlive", "caffeine.tv",
        "flosports", "flo sports", "triller",
        "thursday night football", "monday night football", "sunday ticket",
        "amazon prime video sports", "apple sports", "apple mls",
        "max sports", "peacock live", "paramount+ live",
        "boiler room",
    ],
    # Streaming tech, production, monetization — strong-medium
    6: [
        "transcoder", "video encoder", "live encoder",
        "video cdn", "video delivery",
        "hls streaming", "mpeg-dash", "dash streaming",
        "drm", "widevine", "fairplay", "playready",
        "adaptive bitrate", "abr streaming",
        "ad pod", "ad break", "ad insertion",
        "creator economy", "creator monetization",
        "virtual concert", "livestream concert", "livestreamed concert",
        "esports broadcast", "esports stream", "esports rights",
        "watch party", "co-streaming", "co streaming",
        "rtmp", " srt ", "cmaf",
        "svod", "avod", "tvod", "fast tv",
        "vod platform", "vmvpd",
        "live sports", "live nfl", "live nba", "live mlb", "live soccer",
    ],
    # Streaming-adjacent — medium
    3: [
        "streaming service", "streaming platform", "streaming app",
        "streaming wars", "cord cutter", "cord cutting", "cord-cutting",
        "subscription video", "ad-supported tv", "ad-supported streaming",
        "media rights", "tv rights", "sports rights", "rights deal",
        "broadcaster", "broadcasting deal",
        "connected tv", "smart tv", "ctv ad", " ctv ",
        "video advertising", "video ads",
        "creator platform",
        "live audio", "live music", "live concert",
        "live events platform", "live experience",
        "set-top box",
    ],
    # Weak / contextual — useful only when stacked with other matches
    1: [
        "netflix", "disney+", "disney plus", "hbo",
        "hulu", "max ", "peacock", "paramount+", "paramount plus",
        "apple tv+", "apple tv plus",
        "youtube", "spotify", "tidal",
        "streaming", "broadcast", "broadcaster", "streamer",
        "live video", "live audio",
        "creator", "encoder", "cdn",
        "media company",
    ],
}


# Strong penalty — these terms make an article very unlikely to be relevant.
# Each match subtracts 8 from the keyword score.
NEGATIVE_KEYWORDS = [
    # Fight night noise (we care about distribution, not who punched whom)
    "weigh-in", "weigh in", "weigh ins", "weighed in",
    "fight card", "fight purse", "fight night results",
    "scorecard", " knockout ", "knocked out", "submission win",
    "drug test failure", "failed drug test", "usada",
    "fighter signs", "fighter signed", "fighter released",
    # Recap noise
    "final score", "match recap", "game recap", "post-game",
    "transfer news", "trade rumor", "trade rumors",
    "season finale recap", "episode recap", "season recap",
    # On-demand entertainment noise
    "movie review", "tv review", "show review",
    "spotify wrapped", "song of the year", "album of the year",
    # Commerce / deals noise
    "deal of the day", "best deals", "amazon deals",
    "prime day deals", "black friday deals",
    "hands-on review", "phone review",
]


# Hard-block patterns on the HEADLINE only. If every token in a tuple appears in
# the title (case-insensitive substring match), the article is dropped outright
# regardless of keyword score. Use this for clickbait/promo patterns where each
# word alone would have too many false positives.
TITLE_BLOCKLIST = [
    ("watch", "for free"),
]


INTEREST_PROFILE = """We are myStaze, a live streaming platform. We care about the LIVE STREAMING and BROADCASTING industry - how live content is distributed, monetized, and consumed.

HIGH-VALUE (8-10):
- Live streaming platforms: Twitch, Kick, YouTube Live, TikTok Live, DAZN, ESPN+, UFC Fight Pass, MLB.tv, NBA League Pass, Veeps, Stage+, FloSports, Triller, Boiler Room. Platform launches, feature changes, monetization changes, exits, M&A.
- Broadcast / streaming RIGHTS DEALS: who wins what, fees, exclusivity, geographic splits, length, sub-licensing.
- Live streaming TECH: low-latency protocols (LL-HLS, WebRTC, CMAF, SRT), encoding, CDNs, DRM, server-side ad insertion, multi-angle, interactive features, AI in live production, captions/translation.
- Live sports DISTRIBUTION across NFL, NBA, MLB, NHL, EPL, UEFA, F1, UFC, boxing PPVs, ONE, PFL - when about how the content reaches viewers, not match results.
- Live music streaming: concerts, festivals, DJ sets and shows on Twitch/YouTube, paid livestream concerts, livestream tours.
- Live performing arts streaming: theatre, opera, comedy specials, livestreamed events.
- Creator economy as it touches live streaming.

PREFERRED VERTICAL: combat sports - but ONLY when the story is about broadcasting, streaming, rights, platforms, distribution, or business. Score high when relevant.

LOW-VALUE (1-3):
- Fight cards, fight previews, fighter rankings, results, signings/releases, drug tests, weigh-ins, retirements.
- Match recaps, standings, transfer news, player stats, game previews with no broadcasting/distribution angle.
- On-demand music streaming (Spotify, Apple Music product/business news) UNLESS about live audio, concerts, or live distribution.
- TV/film streaming product news (Netflix subscriber numbers, show cancellations, on-demand catalogue moves) UNLESS it intersects with live distribution or sports rights.
- Generic gadget reviews, consumer deals, commerce.

A useful test: would this article help us understand how live content is distributed, priced, or technically delivered? Yes -> score high. About who won, what someone released on Spotify, or which phone is best -> score low."""


DIGEST_CONFIG = {
    "streaming": {
        "title": "Live Streaming & Broadcasting Daily",
        "emoji": "\U0001F4E1",
        "send_time": "06:00",
        "recipients": [
            "pasi.siitonen@gmail.com",
            "olli.karikoski@mystaze.com",
            "joonas.palkonen@mystaze.com",
            "bjorn.masalin@gmail.com",
            "sarah@wavelength.now",
            "al@extremeinternational.com",
        ],
        # Keyword pre-filter: minimum keyword score to be passed to AI.
        "keyword_threshold": 2,
        # Cap on articles sent to AI per run (top N by keyword score).
        "ai_score_limit": 120,
        # Cap on articles included in the final digest (top N by AI score).
        "digest_limit": 40,
        # AI must score >= this for an article to appear in the digest.
        "ai_min_score": 4,
    },
}
