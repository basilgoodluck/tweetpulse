# scheduler.py
import schedule
import time
import asyncio
from main import main

def job():
    asyncio.run(main())

schedule.every(10).minutes.do(job)

print("Scheduler started. Running every 10 minutes...")
while True:
    schedule.run_pending()
    time.sleep(1)