import os
import time
import schedule
from datetime import datetime, timezone

import startup
from bot import run_digest
from feeds import DIGEST_CONFIG

print("News Bot starting...")
for topic, config in DIGEST_CONFIG.items():
    send_time = os.environ.get(f"SEND_TIME_{topic.upper()}", config["send_time"])
    print(f"  {topic}: daily at {send_time} UTC")
    schedule.every().day.at(send_time, "UTC").do(run_digest, topic)

if os.environ.get("RUN_ON_START", "").lower() == "true":
    topic = os.environ.get("RUN_TOPIC", "")
    if topic:
        print(f"RUN_ON_START with topic={topic}")
        run_digest(topic)
    else:
        print("RUN_ON_START - running all digests")
        for topic in DIGEST_CONFIG:
            run_digest(topic)

print("Entering schedule loop...")
while True:
    try:
        schedule.run_pending()
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] Schedule error: {e}")
    time.sleep(30)
