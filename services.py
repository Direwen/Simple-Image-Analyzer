import os
import datetime
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session

import models
import schemas


class ImageAnalyzer:
    """
    A service class to handle all image analysis logic.
    """

    def __init__(self, img_color: np.ndarray):
        # Store the original color image
        self.img_color = img_color
        # Pre-analyze
        self.perform_analysis()

    def perform_analysis(self):
        try:
            # Convert the image color to gray scale and store it
            self.img_gray = cv2.cvtColor(self.img_color, cv2.COLOR_BGR2GRAY)
            # Calculate the average brightness
            self.avg_brightness = float(np.mean(self.img_gray))
            # Get min/max values and locations
            self.min_val, self.max_val, self.min_loc, self.max_loc = cv2.minMaxLoc(
                self.img_gray
            )
        except cv2.error as e:
            # Handle OpenCV errors
            raise ValueError(f"OpenCV processing error: {e}")
        except Exception as e:
            # Handle any other unexpected errors
            raise ValueError(f"An unexpected error occurred: {e}")

    def get_analysis_data(self) -> Dict[str, Any]:
        """
        Returns a dictionary of the core analysis results.
        """
        return {
            "average_brightness": self.avg_brightness,
            "brightest_point": list(self.max_loc),
            "darkest_point": list(self.min_loc),
            "brightest_value": float(self.max_val),
            "darkest_value": float(self.min_val),
        }

    def get_processed_image_with_highlights(self) -> np.ndarray:
        """
        Draws highlights on a copy of the original image and returns it.
        """
        
        # Create a copy of the original color image
        img_with_highlights = self.img_color.copy()

        # Draw a red circle at the brightest location (BGR)
        cv2.circle(
            img=img_with_highlights,
            center=self.max_loc,
            radius=10,
            color=(0, 0, 255),
            thickness=2,
            lineType=cv2.LINE_AA,
        )
        
        # Draw a blue circle at the darkest location (BGR)
        cv2.circle(
            img=img_with_highlights,
            center=self.min_loc,
            radius=10,
            color=(255, 0, 0),
            thickness=2,
            lineType=cv2.LINE_AA,
        )

        return img_with_highlights

    @staticmethod
    def save_image(
        img_arr: np.ndarray, 
        output_dir: str, 
        base_filename: str
    ) -> Tuple[str, str]:
        
        """
        Saves a NumPy image array to a file with a unique timestamp.
        Returns the (filename, full_save_path).
        """
        
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        # Add a timestamp to the filename to be unique
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize filename to avoid path traversal issues
        safe_filename = Path(base_filename).name
        # Replace spaces with underscores to avoid URL encoding issues
        safe_filename = safe_filename.replace(" ", "_")
        filename = f"output_{timestamp}_{safe_filename}"

        save_path = os.path.join(output_dir, filename)

        try:
            cv2.imwrite(save_path, img_arr)
            return filename, save_path
        except Exception as e:
            # Handle potential file system errors
            raise IOError(f"Could not save image to {save_path}: {e}")


def create_analysis_record(
    db: Session, 
    analysis_data: schemas.AnalysisRecordBase
) -> models.AnalysisRecord:
    
    """
    Create a new analysis record in the database.
    """

    # Convert Pydantic schema to a dictionary
    db_record_data = analysis_data.model_dump()

    # Create the SQLAlchemy model instance
    db_record = models.AnalysisRecord(**db_record_data)

    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
