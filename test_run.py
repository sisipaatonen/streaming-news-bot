import os, sys
sys.path.insert(0, "/home/pasi/streaming-news-bot")
os.chdir("/home/pasi/streaming-news-bot")
os.environ["GMAIL_TOKEN_PATH"] = "/home/pasi/.config/assistant/gmail_token.pickle"
os.environ["GMAIL_USER"] = "pasi.siitonen@gmail.com"
os.environ["DB_PATH"] = "/tmp/news_test.db"

# To test with AI scoring, set your API key:
# os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."

from bot import run_digest
import sys as _sys

topic = _sys.argv[1] if len(_sys.argv) == 2 else "streaming"
print(f"Starting test run for topic: {topic}")
run_digest(topic)
print("Done!")
