import os
import uuid

import requests
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime

from celery import Celery

celery = Celery('tasks', broker='pyamqp://guest:guest@rabbitmq//', backend='rpc://')

reports_dir = os.environ.get("REPORTS_DIR", "/app/reports")

@celery.task
def generate_disney_report():
    report_id = uuid.uuid4()

    api_url = "https://api.disneyapi.dev/character"
    response = requests.get(api_url)
    data = response.json()

    characters = data.get("data", [])

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("disney.html.j2")

    rendered_html = template.render(characters=characters)

    current_datetime = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')
    report_filename = f"{report_id}-{current_datetime}"
    rendered_html_output_path = os.path.join(reports_dir, f"{report_filename}.html")

    with open(rendered_html_output_path, "w", encoding="utf-8") as output_file:
        output_file.write(rendered_html)

    print("HTML template has been rendered and saved to output.html.")

    rendered_pdf_output_path = os.path.join(reports_dir, f"{report_filename}.pdf")
    HTML(string=rendered_html).write_pdf(rendered_pdf_output_path)
    print("PDF file has been generated.")

    return report_filename
