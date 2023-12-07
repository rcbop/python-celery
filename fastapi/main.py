from celery.result import AsyncResult

import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from report import celery, generate_disney_report

app = FastAPI()

reports_dir = os.environ.get("REPORTS_DIR", "/app/reports")

@app.post("/generate-report")
async def generate_report():
    task_result = generate_disney_report.delay()

    return {"task_id": task_result.id}


@app.get("/check-task/{task_id}")
async def check_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery)
    print(task_result)

    if task_result.ready():
        return {"status": "completed", "result": task_result.result}
    else:
        return {"status": "pending"}


@app.get("/download-report/{task_id}")
async def download_report(task_id: str):
    task_result = AsyncResult(task_id, app=celery)

    if task_result.ready():
        report_path = os.path.join(reports_dir, f"{task_result.result}.pdf")
        return FileResponse(report_path, media_type="application/pdf", filename=f"{task_result.result}.pdf")
    else:
        return {"status": "pending"}
