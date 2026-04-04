FEEDS = [
    # Music streaming
    {"name": "Music Business Worldwide", "url": "https://www.musicbusinessworldwide.com/feed/", "category": "music"},
    {"name": "Music Ally", "url": "https://musically.com/feed/", "category": "music"},

    # Entertainment / streaming platforms
    {"name": "Variety", "url": "https://variety.com/feed/", "category": "entertainment"},
    {"name": "Deadline", "url": "https://deadline.com/feed/", "category": "entertainment"},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/feed/", "category": "entertainment"},

    # Streaming tech
    {"name": "Next TV", "url": "https://www.nexttv.com/rss.xml", "category": "streaming"},
    {"name": "TV Tech", "url": "https://www.tvtechnology.com/rss.xml", "category": "streaming"},

    # Sports streaming
    {"name": "SportsPro Media", "url": "https://www.sportspromedia.com/feed/", "category": "sports"},

    # From tech-news-bot
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "category": "tech"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "category": "tech"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "category": "tech"},
    {"name": "Phoronix", "url": "https://www.phoronix.com/rss.php", "category": "tech"},
    {"name": "Ubuntu Blog", "url": "https://ubuntu.com/blog/feed", "category": "tech"},
    {"name": "Python Insider", "url": "https://blog.python.org/feeds/posts/default?alt=rss", "category": "tech"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "category": "tech"},
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/", "category": "tech"},
    {"name": "Venture Beat", "url": "https://venturebeat.com/feed/", "category": "tech"},
]

# Keywords for scoring relevance
KEYWORDS_HIGH = [
    "streaming", "spotify", "apple music", "tidal", "youtube music", "deezer",
    "netflix", "disney+", "hbo", "amazon prime", "live stream", "twitch",
    "sports rights", "broadcast rights", "ott", "subscription", "royalties",
    "music rights", "licensing", "platform", "pay-per-view", "ppv",
    "nfl", "nba", "premier league", "champions league", "formula 1",
    "direct-to-consumer", "cord cutting", "4k stream", "latency", "cdn",
    "ai", "llm", "open source", "linux", "python", "developer"
]

KEYWORDS_MEDIUM = [
    "music", "artist", "label", "revenue", "rights", "digital", "tech",
    "app", "launch", "deal", "partnership", "merger", "acquisition",
    "video", "audio", "podcast", "radio", "broadcast", "media",
    "software", "hardware", "release", "update", "api"
]
