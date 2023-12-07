import datetime
import os
import time

import schedule

reports_dir = os.environ.get("REPORTS_DIR", "/app/reports")
max_days_to_keep_reports = os.environ.get("MAX_DAYS_TO_KEEP_REPORTS", 7)

def clean_up_reports():
    print("Cleaning up reports")

    for filename in os.listdir(reports_dir):
        # the filename is something like 123e4567-e89b-12d3-a456-426614174000-2021-08-01T12:00:00.pdf
        if filename.endswith(".pdf"):
            report_date = filename.split("-")[-1].split(".")[0]
            report_datetime = datetime.strptime(report_date, "%Y-%m-%dT%H:%M:%S")
            current_datetime = datetime.now()
            difference = current_datetime - report_datetime
            if difference.days > max_days_to_keep_reports:
                os.remove(os.path.join(reports_dir, filename))

def start_cleaner():
    schedule.every(10).minutes.do(clean_up_reports)

if __name__ == "__main__":
    print("Starting cleaner")
    start_cleaner()

    while True:
        schedule.run_pending()
        time.sleep(1)
