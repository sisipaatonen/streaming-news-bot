FEEDS = [
    # Music streaming
    {"name": "Music Business Worldwide", "url": "https://www.musicbusinessworldwide.com/feed/", "category": "music", "topics": ["streaming"]},
    {"name": "Music Ally", "url": "https://musically.com/feed/", "category": "music", "topics": ["streaming"]},

    # Entertainment / streaming platforms
    {"name": "Variety", "url": "https://variety.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Deadline", "url": "https://deadline.com/feed/", "category": "entertainment", "topics": ["streaming"]},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/feed/", "category": "entertainment", "topics": ["streaming"]},

    # Streaming tech
    {"name": "Next TV", "url": "https://www.nexttv.com/rss.xml", "category": "streaming", "topics": ["streaming"]},
    {"name": "TV Tech", "url": "https://www.tvtechnology.com/rss.xml", "category": "streaming", "topics": ["streaming"]},

    # Sports streaming
    {"name": "SportsPro Media", "url": "https://www.sportspromedia.com/feed/", "category": "sports", "topics": ["streaming"]},

    # Tech feeds
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "category": "tech", "topics": ["tech"]},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "category": "tech", "topics": ["tech", "streaming"]},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "category": "tech", "topics": ["tech", "streaming"]},
    {"name": "Phoronix", "url": "https://www.phoronix.com/rss.php", "category": "tech", "topics": ["tech"]},
    {"name": "Ubuntu Blog", "url": "https://ubuntu.com/blog/feed", "category": "tech", "topics": ["tech"]},
    {"name": "Python Insider", "url": "https://blog.python.org/feeds/posts/default?alt=rss", "category": "tech", "topics": ["tech"]},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "category": "tech", "topics": ["tech"]},
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/", "category": "tech", "topics": ["tech"]},
    {"name": "Venture Beat", "url": "https://venturebeat.com/feed/", "category": "tech", "topics": ["tech", "streaming"]},
]


# Interest profiles for AI scoring per topic
INTEREST_PROFILES = {
    "streaming": """Live streaming platforms and technology. Music streaming services (Spotify, Apple Music, Tidal, YouTube Music, Deezer).
Video streaming (Netflix, Disney+, HBO, Amazon Prime). Sports streaming and live events.
Music industry business, royalties, licensing, rights management.
Content delivery networks, encoding, low-latency streaming tech.
myStaze Music - a live streaming platform for music artists.""",

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
        "title": "Streaming News Daily",
        "emoji": "📡",
        "recipients": [
            "pasi.siitonen@gmail.com",
            "olli.karikoski@mystaze.com",
            "joonas.palkonen@mystaze.com",
        ],
        "send_time": "06:00",
        "category_order": ["music", "streaming", "sports", "entertainment", "tech"],
        "category_labels": {
            "music": "🎵 Music Streaming",
            "streaming": "📺 Streaming Platforms & Tech",
            "tech": "💻 Tech",
            "sports": "⚽ Sports Streaming",
            "entertainment": "🎬 Entertainment",
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
