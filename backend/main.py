import shutil
import os
import sys
import subprocess
import pandas as pd

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from validate_license import validate

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])



if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/license-status")
def license_status():
    import traceback

    try:
        return validate()

    except Exception as e:
        traceback.print_exc()

        return {
            "status": "ERROR",
            "message": repr(e)
        }

@app.post("/upload-license")
async def upload_license(file: UploadFile = File(...)):
    try:
        license_path = os.path.join(BASE_DIR, "license.lic")
        with open(license_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        status = validate()
        return status
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/preview")
async def preview(file: UploadFile = File(...)):
    print("Preview API Called")
    file_path = os.path.join(INPUT_FOLDER, "uploaded_input.xlsx")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Initial batch processing for preview
    batch_exe = os.path.join(BASE_DIR, "batch.exe")
    result = subprocess.run(
        [batch_exe, "5", "3"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {"status": "ERROR", "stderr": result.stderr}

    preview_file = os.path.join(OUTPUT_FOLDER, "scheduler_input.xlsx")
    df = pd.read_excel(preview_file)

    # Batches numeric conversion
    df["BATCHES"] = pd.to_numeric(df["BATCHES"], errors="coerce").fillna(0)

    # Bay 2 Table
    bay2_df = df[df["BAY"] == 2].sort_values(by="BATCHES", ascending=False)

    # Bay 3 Table
    bay3_df = df[df["BAY"] == 3].sort_values(by="BATCHES", ascending=False)

    return {
        "bay2": bay2_df.fillna("").to_dict(orient="records"),
        "bay3": bay3_df.fillna("").to_dict(orient="records")
    }
@app.post("/generate")
async def generate(
    file: UploadFile = File(...),
   
):
    # Save uploaded file
    file_path = os.path.join(INPUT_FOLDER, "uploaded_input.xlsx")
    bay2 = 5
    bay3 = 3

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    scheduler_exe = os.path.join(
        BASE_DIR,
        "scheduling_basic_loading_plotting_v7.exe"
)

    try:
        # Run Python scheduler
        subprocess.run(
            [
                scheduler_exe,
                str(bay2),
                str(bay3)
            ],
            check=True
        )

        output_file = os.path.join(
            OUTPUT_FOLDER,
            "scheduler_output.xlsx"
        )

        if not os.path.exists(output_file):
            return {
                "status": "ERROR",
                "message": "Scheduler output not found"
            }

        df = pd.read_excel(output_file)

        return df.fillna("").to_dict(orient="records")

    except subprocess.CalledProcessError as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
    
    
@app.get("/download")
def download():
    output_file = os.path.join(OUTPUT_FOLDER, "scheduler_output.xlsx")
    if os.path.exists(output_file):
        return FileResponse(output_file, filename="scheduler_output.xlsx")
    return {"status": "ERROR", "message": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)