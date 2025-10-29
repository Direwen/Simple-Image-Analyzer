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
        
        # Convert the bytes of img into np array of uint8 (1D)
        nparr = np.frombuffer(image_in_bytes, np.uint8)
        # Decodes nparr into the actual image matrix (3D)
        img_color = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if not img_color:
            raise HTTPException(
                status_code=400,
                detail="Invalid image file or unsupported format."
            ) 
        
        img_analyzer = ImageAnalyzer(img_color)
        analysis = img_analyzer.get_analysis_data()
        processed_image_arr = img_analyzer.get_processed_image_with_highlights()
        # filename, save_path = ImageAnalyzer.save_image(
        #     processed_image_arr, 
        #     RESULTS_DIR, 
        #     file.filename
        # )
        # processed_url = request.url_for('results', path=filename)
        return {
            **analysis,
        }
        
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    
    # 4. The API should be fully testable via Swagger/OpenApi UI at /docs.
    # 5. Store the analysis results in a MySQL database with columns: id, filename, average_brightness, brightest_value, darkest_value, created_at
    # 6. Include a /download/{filename} endpoint to download the processed image.