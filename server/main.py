import os
import tempfile
from collections import Counter
import zipfile
from fastapi import FastAPI, UploadFile, File
from fastapi.params import Form
from starlette.responses import JSONResponse, FileResponse
from analysis_utils import plot_histogram, plot_pie, plot_bar, plot_issue_trend, analyze_code
app=FastAPI()

@app.get("/")
async def hello():
    return {"welcome":"Hi😄"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...),history_dir_path: str = Form(...)
):
        filename = file.filename
        if not filename.endswith(".py"):
            return JSONResponse({"error": "Only Python (.py) files are supported."}, status_code=400)

        HISTORY_DIR = os.path.join(history_dir_path, ".wit", "issues_history")
        os.makedirs(HISTORY_DIR, exist_ok=True)


        code = (await file.read()).decode("utf-8")
        analysis_result = analyze_code(code, filename,HISTORY_DIR)
        issues = analysis_result["issues"]
        function_lengths = analysis_result["function_lengths"]

        # Prepare data for graphs
        issue_counts = {k: len(v) for k, v in issues.items()}
        total_issues = sum(issue_counts.values())
        issues_per_file = Counter()
        for k, v in issues.items():
            for item in v:
                fname = item.split(":")[0]
                issues_per_file[fname] += 1

        # create a temporary directory
        tempdir = tempfile.mkdtemp()

        # Generate all graph images
        hist_path = os.path.join(tempdir, "histogram.png")
        if function_lengths:
            plot_histogram(function_lengths.values(), hist_path)
        else:
            print("לא נמצאו פונקציות בקובץ, לא נצייר היסטוגרמה.")

        pie_path = os.path.join(tempdir, "pie.png")
        plot_pie(issue_counts, pie_path)

        bar_path = os.path.join(tempdir, "bar.png")
        plot_bar(issues_per_file, bar_path)

        # Bonus: plot trend over time (dummy data for example)
        trend_path = os.path.join(tempdir, "trend.png")
        log_path = os.path.join(HISTORY_DIR, "analysis_log.csv")
        plot_issue_trend(log_path, trend_path)

        # Create zip file
        zip_path = os.path.join(tempdir, "analysis_graphs.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(hist_path, arcname="histogram.png")
            zipf.write(pie_path, arcname="pie.png")
            zipf.write(bar_path, arcname="bar.png")
            zipf.write(trend_path, arcname="trend.png")

        # Return the zip file as a downloadable response
        return FileResponse(zip_path, filename="analysis_graphs.zip", media_type='application/zip')


@app.post("/alerts")
async def code_alerts(file: UploadFile = File(...),history_dir_path: str = Form(...)):
    filename = file.filename
    if not filename.endswith(".py"):
        return JSONResponse({"error": "Only Python (.py) files are supported."}, status_code=400)

    code = (await file.read()).decode("utf-8")
    HISTORY_DIR = os.path.join(history_dir_path, ".wit", "issues_history")
    os.makedirs(HISTORY_DIR, exist_ok=True)
    analysis_result = analyze_code(code, filename,HISTORY_DIR)
    return JSONResponse(content={"issues": analysis_result["issues"]})
