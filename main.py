import os
import time
import schedule
from datetime import datetime
from bot import run

SEND_TIME = os.environ.get("SEND_TIME", "08:00")

def job():
    print(f"[{datetime.now()}] Running scheduled news digest...")
    try:
        run()
    except Exception as e:
        print(f"Error: {e}")

print(f"📡 Streaming News Bot starting — will send daily at {SEND_TIME} Helsinki time")
schedule.every().day.at(SEND_TIME).do(job)

# Run immediately on startup if env says so (for testing)
if os.environ.get("RUN_ON_START", "").lower() == "true":
    print("RUN_ON_START=true — running now...")
    job()

while True:
    schedule.run_pending()
    time.sleep(30)
