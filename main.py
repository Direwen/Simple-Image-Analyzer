import os
from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
import cv2
from services import ImageAnalyzer

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

app = FastAPI(title="Image Analyzer")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file selected")

    filename = file.filename
    
    # Accept only .jpg or .png file
    if not filename.endswith((".jpg", ".png")):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only .jpg and .png files are allowed"
        )
        
    image_in_bytes = await file.read()
    if not image_in_bytes:
        raise HTTPException(
            status_code=400,
            detail="Empty File Found"
        )
    
    try:
        
        pass
        
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    
    # 4. The API should be fully testable via Swagger/OpenApi UI at /docs.
    # 5. Store results in a MySQL database with columns: id, filename, average_brightness, brightest_value, darkest_value, created_at
    # 6. Include a /download/{filename} endpoint to download the processed image.