FEEDS = [
    # Combat sports - PRIMARY FOCUS
    {"name": "MMA Fighting", "url": "https://www.mmafighting.com/rss/index.xml", "category": "combat", "topics": ["streaming"]},
    {"name": "MMA Junkie", "url": "https://mmajunkie.usatoday.com/feed", "category": "combat", "topics": ["streaming"]},
    {"name": "Sherdog", "url": "https://www.sherdog.com/rss/news.xml", "category": "combat", "topics": ["streaming"]},
    {"name": "Bloody Elbow", "url": "https://www.bloodyelbow.com/rss/index.xml", "category": "combat", "topics": ["streaming"]},
    {"name": "BoxingScene", "url": "https://www.boxingscene.com/rss/news.xml", "category": "combat", "topics": ["streaming"]},

    # Live streaming platforms & tech
    {"name": "Next TV", "url": "https://www.nexttv.com/rss.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "TV Tech", "url": "https://www.tvtechnology.com/rss.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "StreamTV Insider", "url": "https://www.streamtvinsider.com/rss/all", "category": "streaming", "topics": ["streaming"]},

    # Sports streaming & business
    {"name": "SportsPro Media", "url": "https://www.sportspromedia.com/feed/", "category": "sports", "topics": ["streaming"]},

    # Entertainment streaming (context)
    {"name": "Variety", "url": "https://variety.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Deadline", "url": "https://deadline.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/feed/", "category": "entertainment", "topics": ["streaming"]},

    # Music streaming - future focus, deprioritized
    {"name": "Music Business Worldwide", "url": "https://www.musicbusinessworldwide.com/feed/", "category": "music", "topics": ["streaming"]},
    {"name": "Music Ally", "url": "https://musically.com/feed/", "category": "music", "topics": ["streaming"]},

    # Cross-listed tech feeds (relevant to both streaming and tech digests)
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "category": "tech", "topics": ["tech", "streaming"]},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "category": "tech", "topics": ["tech", "streaming"]},
    {"name": "Venture Beat", "url": "https://venturebeat.com/feed/", "category": "tech", "topics": ["tech", "streaming"]},

    # Tech-only feeds
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "category": "tech", "topics": ["tech"]},
    {"name": "Phoronix", "url": "https://www.phoronix.com/rss.php", "category": "tech", "topics": ["tech"]},
    {"name": "Ubuntu Blog", "url": "https://ubuntu.com/blog/feed", "category": "tech", "topics": ["tech"]},
    {"name": "Python Insider", "url": "https://blog.python.org/feeds/posts/default?alt=rss", "category": "tech", "topics": ["tech"]},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "category": "tech", "topics": ["tech"]},
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/", "category": "tech", "topics": ["tech"]},
]


# Interest profiles for AI scoring per topic
INTEREST_PROFILES = {
    "streaming": """PRIMARY FOCUS: Combat sports streaming and broadcasting.
- MMA, UFC, Bellator, ONE Championship, PFL, kickboxing, K-1, Glory, professional boxing, BJJ and grappling.
- Combat sports broadcast rights, PPV deals, streaming platform exclusives, fighter pay, promotion business.
- Combat sports streaming platforms: UFC Fight Pass, DAZN, ESPN+, Triller, Fanatiq, Fight Network.

SECONDARY FOCUS: Live streaming landscape - technology, platforms, business models.
- Live streaming infrastructure: low-latency protocols (LL-HLS, WebRTC, CMAF), CDN, encoding, transcoding.
- Live streaming platforms, OTT services, D2C launches, FAST channels.
- Sports streaming rights deals and broadcast distribution globally.
- PPV vs subscription vs ad-supported live, monetization, audience metrics.

CONTEXT: General entertainment streaming (Netflix, Disney+, HBO, Amazon Prime) - only relevant when it informs live streaming or sports rights.

FUTURE INTEREST (lower priority): Music streaming and live music streaming - relevant but not the main focus.

myStaze is a live streaming platform currently focused on combat sports, with future plans to expand into music.""",

    "tech": """Voice-controlled Linux desktop assistant using Claude API, Whisper, openwakeword.
Linux desktop: Ubuntu 24.04, GNOME, Dell XPS 13.
Python development, CLI tools, automation.
AI/ML, large language models, speech recognition, AI agents.
Spotify and YouTube integration on Linux.
Open source tools, developer productivity.""",
}


# Digest configuration per topic
DIGEST_CONFIG = {
    "streaming": {
        "title": "Combat Sports & Live Streaming Daily",
        "emoji": "🥊",
        "recipients": [
            "pasi.siitonen@gmail.com",
            "olli.karikoski@mystaze.com",
            "joonas.palkonen@mystaze.com",
            "bjorn.masalin@gmail.com",
        ],
        "send_time": "06:00",
        "category_order": ["combat", "streaming", "sports", "entertainment", "music", "tech"],
        "category_labels": {
            "combat": "🥊 Combat Sports",
            "streaming": "📺 Live Streaming Platforms & Tech",
            "sports": "🏆 Sports Streaming & Business",
            "entertainment": "🎬 Entertainment Streaming",
            "music": "🎵 Music Streaming (Future)",
            "tech": "💻 Tech",
        },
    },
    "tech": {
        "title": "Tech News Digest",
        "emoji": "💻",
        "recipients": [
            "pasi.siitonen@gmail.com",
        ],
        "send_time": "07:00",
        "category_order": ["tech"],
        "category_labels": {
            "tech": "💻 Tech & AI",
        },
    },
}
