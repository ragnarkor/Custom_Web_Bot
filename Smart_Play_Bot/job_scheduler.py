import schedule
import time
from smart_play_bot import main

def job():
    options_list = ["--disable-gpu",
                    # "--headless",
                    # "--no-sandbox",
                    # "--disable-dev-shm-usage",
                    "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"]

    try:
        main(options_list, keep_alive=True)

    except Exception as e:
        print(e)

# Schedule the job to run every day at 7:00 AM
schedule.every().day.at("07:00").do(job)

while True:
    # Check for any pending jobs and run them
    schedule.run_pending()
    time.sleep(1)  # Sleep for a short time to avoid busy waiting