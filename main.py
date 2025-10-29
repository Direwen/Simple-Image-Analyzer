import os
import cv2
import numpy as np

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path

import models
import schemas
import services
from database import SessionLocal, engine, Base

# tells SQLAlchemy to create the tables
models.Base.metadata.create_all(bind=engine)

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

app = FastAPI(title="Image Analyzer")

# Mount the results directory to serve static files
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="results")

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        # yield the db session to the route handler
        yield db
        # Commit the transaction
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        # close the db session after the request is processed
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/analyze-image")
async def analyze_image(
    request: Request, 
    db: Session = Depends(get_db), 
    file: UploadFile = File(...)
):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file selected")

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .jpg and .png files are allowed",
        )

    image_in_bytes = await file.read()
    if not image_in_bytes:
        raise HTTPException(status_code=400, detail="Empty File Found")

    try:
        # Convert the image bytes to a numpy array of img
        nparr = np.frombuffer(image_in_bytes, np.uint8)
        # Load the image as a color image (BGR)
        img_color = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_color is None:
            raise HTTPException(
                status_code=400,
                detail="Failed to decode image. Please check the file format.",
            )

        img_analyzer = services.ImageAnalyzer(img_color)
        analysis_data = img_analyzer.get_analysis_data()
        processed_image_arr = img_analyzer.get_processed_image_with_highlights()

        saved_filename, save_path = services.ImageAnalyzer.save_image(
            processed_image_arr, RESULTS_DIR, file.filename
        )

        # Create the Pydantic schema for the DB
        record_to_create = schemas.AnalysisRecordBase(
            filename=saved_filename,
            average_brightness=analysis_data["average_brightness"],
            brightest_value=analysis_data["brightest_value"],
            darkest_value=analysis_data["darkest_value"],
        )

        # save to the DB
        db_record = services.create_analysis_record(
            db=db, analysis_data=record_to_create
        )

        # Use mount to get the public URL
        processed_url = request.url_for("results", path=saved_filename)

        return {
            "id": db_record.id,
            "filename": db_record.filename,
            "created_at": db_record.created_at,
            "processed_image_url": str(processed_url),
            **analysis_data,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {e}")
    except IOError as e:
        # Catches file save errors
        raise HTTPException(status_code=500, detail=f"File saving error: {e}")
    except Exception as e:
        # General catch-all
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/download/{filename}")
async def download_image(filename: str):
    """
    Provides a download link for a processed image.
    """
    # Path sanitization to prevent directory access
    safe_filename = Path(filename).name
    print(f"safe_filename: {safe_filename}")

    # Construct the full path to the file
    file_path = os.path.join(RESULTS_DIR, safe_filename)
    print(f"file_path: {file_path}")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, media_type="image/png", filename=safe_filename)
