import os
import uuid
from datetime import datetime
from queue import Queue
from threading import Thread
import gc

import requests
from jinja2 import Environment, FileSystemLoader
from retry import retry
from weasyprint import HTML

from celery import Celery

celery = Celery(
    'tasks', broker='pyamqp://guest:guest@rabbitmq//', backend='rpc://')

reports_dir = os.environ.get("REPORTS_DIR", "/app/reports")
pages = os.environ.get("PAGES", 5)


@retry(exceptions=Exception, tries=3, delay=1, backoff=2, max_delay=4)
def make_request(page_size, page_number, result_queue):
    print(f"Making request for page {page_number} of size {page_size}.")
    api_url = f"https://api.disneyapi.dev/character?pageSize={page_size}&page={page_number}"
    response = requests.get(api_url)
    print(f"Request page {page_number} got response {response.status_code}")
    response.raise_for_status()
    data = response.json()
    characters = data.get("data", [])
    result_queue.put(characters)


def get_report_data():
    result_queue = Queue()

    threads = []
    for i in range(1, pages + 1):
        thread = Thread(target=make_request, args=(100, i, result_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    all_characters = []
    while not result_queue.empty():
        all_characters.extend(result_queue.get())

    return all_characters


@celery.task
def generate_disney_report():
    try:
        report_id = uuid.uuid4()

        start_time = datetime.now()
        print(f"Started report {report_id} at {start_time}.")

        characters = get_report_data()

        print(f"Report {report_id} has {len(characters)} characters.")

        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("disney.html.j2")

        rendered_html = template.render(characters=characters)

        current_datetime = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')
        report_filename = f"{report_id}-{current_datetime}"
        rendered_html_output_path = os.path.join(
            reports_dir, f"{report_filename}.html")

        with open(rendered_html_output_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_html)

        print("HTML template has been rendered and saved to output.html.")

        rendered_pdf_output_path = os.path.join(
            reports_dir, f"{report_filename}.pdf")

        print("Generating PDF report.")
        HTML(string=rendered_html).write_pdf(rendered_pdf_output_path)
        print(f"PDF report has been saved to {rendered_pdf_output_path}.")
        print(f"Ellapsed time: {datetime.now() - start_time}")

        return report_filename
    finally:
        gc.collect()

