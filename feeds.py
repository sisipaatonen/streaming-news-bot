"""News sources, keyword filters, and interest profiles for the daily digest.

The digest has TWO categories rendered as separate sections in one email:

  1. "streaming" — broad source list (general tech + media + sports + music +
     community), tight streaming-specific keywords. Surfaces live-streaming and
     broadcasting industry news wherever it appears.

  2. "tech" — small, carefully vetted source list, looser tech keywords aimed
     at cutting-edge tech a startup founder/CTO would want to know about.

Each category is independently filtered, AI-scored, and ranked. Cross-section
dedup means an article only ever appears in one section per email.
"""

# --- Feed sources -----------------------------------------------------------

# General tech publications. Eligible for BOTH categories — an AI article from
# TechCrunch lands in tech; a Twitch article from TechCrunch lands in streaming.
GENERAL_TECH_FEEDS = [
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"},
    {"name": "Wired", "url": "https://www.wired.com/feed/rss"},
    {"name": "VentureBeat", "url": "https://venturebeat.com/feed/"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage"},
    {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
    {"name": "The Information (free)", "url": "https://www.theinformation.com/feed"},
    {"name": "IEEE Spectrum", "url": "https://spectrum.ieee.org/feeds/feed.rss"},
]

# Streaming-only sources — consumer gadget pubs, media trade, sports business,
# music industry, community signals. Eligible only for the streaming category.
STREAMING_ONLY_FEEDS = [
    # Consumer tech (kept here, not in tech category — too much gadget/review noise)
    {"name": "Engadget", "url": "https://www.engadget.com/rss.xml"},
    {"name": "Mashable", "url": "https://mashable.com/feeds/rss/all"},
    {"name": "TechRadar", "url": "https://www.techradar.com/rss"},
    {"name": "ZDNet", "url": "https://www.zdnet.com/news/rss.xml"},
    {"name": "9to5Mac", "url": "https://9to5mac.com/feed/"},
    {"name": "9to5Google", "url": "https://9to5google.com/feed/"},

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

# Union of all feeds we actually fetch.
FEEDS = GENERAL_TECH_FEEDS + STREAMING_ONLY_FEEDS

STREAMING_SOURCES = {f["name"] for f in GENERAL_TECH_FEEDS + STREAMING_ONLY_FEEDS}
TECH_SOURCES = {f["name"] for f in GENERAL_TECH_FEEDS}


# --- Streaming category: keywords + profile ---------------------------------

# Title matches count double. Higher weight = stronger signal that the article
# is about live streaming or broadcasting in a way we care about.
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


# Strong penalty for the streaming category — each match subtracts 8.
STREAMING_NEGATIVE_KEYWORDS = [
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


STREAMING_INTEREST_PROFILE = """We are myStaze, a live streaming platform. We care about the LIVE STREAMING and BROADCASTING industry - how live content is distributed, monetized, and consumed.

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


# --- Tech category: keywords + profile --------------------------------------

# Looser keyword set — the sources are already vetted, so we cast a wider net
# and let the AI ranker do the heavy lifting.
TECH_KEYWORDS = {
    # Strong startup / cutting-edge signals
    8: [
        "raises", "series a", "series b", "series c", "series d",
        "seed round", "funding round", "led by", "valuation",
        "startup", "founder", "founders", "y combinator", " yc ",
        "ai model", "frontier model", "foundation model",
        "llm", " gpt-", "gpt-4", "gpt-5", "claude", "gemini", "llama",
        "mistral", "deepseek", "grok",
        "open source",
        "breakthrough", "world first", "first ever",
        "agentic", "ai agent", "ai agents",
    ],
    # Cutting-edge tech & developer tools
    5: [
        "artificial intelligence", "machine learning", "neural network",
        "generative ai", "reasoning model", "multimodal",
        "developer tool", " api ", " sdk ", "framework",
        "open weights", "open-weights",
        "chip", " gpu ", "silicon", "semiconductor", "tpu",
        "quantum computing", "quantum chip",
        "robot", "robotics", "humanoid", "autonomous vehicle", "self-driving",
        " ar ", " vr ", " xr ", "mixed reality", "spatial computing",
        "biotech", "synthetic biology", "crispr",
        "fusion", "battery breakthrough", "solid-state battery",
        "cybersecurity", "zero-day", "vulnerability disclosed",
        "research paper", "arxiv",
        "edge ai", "on-device ai",
        "data center", "hyperscaler",
    ],
    # Broad tech happenings
    3: [
        "tech startup", "platform launch", "launches", "unveils",
        "announces", "introduces",
        "product launch", "new feature",
        "acquisition", "acquires", "ipo",
        "open-source", "github", "developer platform",
        "infrastructure", "compute",
        "cloud", "saas", "paas",
    ],
}


TECH_NEGATIVE_KEYWORDS = [
    # Consumer commerce / deal-hunting noise
    "best deals", "deal of the day", "amazon deals",
    "prime day deals", "black friday deals",
    "best buy deal", "walmart deal",
    "gift guide", "holiday gift",
    # Reviews / listicles
    "tv review", "show review", "movie review",
    "phone review", "hands-on review",
    "best laptop", "best phone", "best headphones",
    "vs ", "comparison: ",
    "tips and tricks", "how to ",
    # Plot / entertainment recap noise
    "episode recap", "season finale", "movie trailer",
    "tv trailer", "watch the trailer",
    # Speculation
    "rumor: ", "leak: ", "leaked images",
    "could be", "might be", "expected to",
]


TECH_INTEREST_PROFILE = """We are a tech-savvy team looking for a daily pulse on CUTTING-EDGE TECHNOLOGY relevant to startups. We want to stay sharp on what's possible and what serious operators are paying attention to.

HIGH-VALUE (8-10):
- AI / ML breakthroughs: new frontier models, novel architectures, significant capability jumps, major research papers, agentic systems.
- Foundation model news (OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral, xAI, DeepSeek, etc.) and how it shifts what's buildable.
- Developer tools / platforms that change how startups ship: new SDKs, APIs, frameworks, devex wins, open-source releases that move the field.
- Startup funding rounds in AI, robotics, biotech, energy, deep tech — what category did smart capital just back, and at what scale?
- Cutting-edge hardware: novel chips, GPUs, TPUs, quantum, photonics, robotics, autonomous systems, on-device AI.
- Platform shifts and emerging categories that could become the next big thing (spatial computing, agentic AI, edge compute, neural interfaces, etc.).
- Significant cybersecurity events that startups should know about (major vulnerabilities, breaches affecting infra).

MEDIUM-VALUE (5-7):
- Big-tech strategy moves (Microsoft / Google / Apple / Meta) when they signal a platform shift, not earnings or product polish.
- Notable acquisitions in deep tech, AI, or developer tooling.
- Important regulation that meaningfully constrains or enables AI/tech startups.

LOW-VALUE (1-3):
- Consumer gadget reviews, deals, holiday shopping, accessory roundups.
- Phone leaks, rumors, spec sheets, unboxings, "best of" listicles, "how to" tutorials.
- Show/plot recaps, on-demand streaming releases, entertainment news.
- Crypto/web3 hype unless tied to real infrastructure or AI compute.
- Pure earnings reporting without strategy signal.

A useful test: would a tech founder or CTO want to know this TODAY to stay sharp on what's possible or where the field is moving? Yes -> high. Is it a deal page, a leak, a phone review, or a listicle? -> low."""


# --- Hard title blocklist ---------------------------------------------------

# Hard-block patterns on the HEADLINE. If every token in a tuple appears in the
# title (case-insensitive substring match), the article is dropped outright
# regardless of keyword score or category. Use this for clickbait/promo
# patterns where each word alone would have too many false positives.
TITLE_BLOCKLIST = [
    ("how to watch",),
    ("watch", "for free"),
]


# --- Digest config ----------------------------------------------------------

DIGEST_CONFIG = {
    "streaming": {
        "title": "myStaze Daily Brief",
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
        # Categories are processed in order. An article assigned to an earlier
        # category will not appear in a later one.
        "categories": [
            {
                "key": "streaming",
                "title": "Live Streaming & Broadcasting",
                "emoji": "\U0001F4E1",
                "sources": STREAMING_SOURCES,
                "keywords": STREAMING_KEYWORDS,
                "negative_keywords": STREAMING_NEGATIVE_KEYWORDS,
                "interest_profile": STREAMING_INTEREST_PROFILE,
                "keyword_threshold": 2,
                "ai_score_limit": 120,
                "digest_limit": 25,
                "ai_min_score": 4,
            },
            {
                "key": "tech",
                "title": "Hot Tech for Startups",
                "emoji": "\U0001F680",
                "sources": TECH_SOURCES,
                "keywords": TECH_KEYWORDS,
                "negative_keywords": TECH_NEGATIVE_KEYWORDS,
                "interest_profile": TECH_INTEREST_PROFILE,
                "keyword_threshold": 1,
                "ai_score_limit": 80,
                "digest_limit": 15,
                "ai_min_score": 5,
            },
        ],
    },
}
