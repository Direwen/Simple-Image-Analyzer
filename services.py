import datetime
import os
from typing import Dict, Any, Tuple
import cv2
import numpy as np
from pathlib import Path

class ImageAnalyzer:
    """
    A service class to handle all image processing logic.
    It's initialized with a decoded color image (NumPy array).
    """
    
    def __init__(self, img_color: np.ndarray):
        if img_color is None or img_color.size == 0:
            raise ValueError("Invalid image data provided to ImageAnalyzer.")
            
        self.img_color = img_color
        
        self.perform_analysis()
    
    def perform_analysis(self):
        try:
            # Convert the image color to gray scale
            self.gray = cv2.cvtColor(self.img_color, cv2.COLOR_BGR2GRAY)
            # Calculate the average brightness
            self.avg_brightness = float(np.mean(self.gray))
            # Get min/max values and locations
            self.min_val, self.max_val, self.min_loc, self.max_loc = cv2.minMaxLoc(self.gray)
        except cv2.error as e:
            # Handle OpenCV errors
            raise ValueError(f"OpenCV processing error: {e}")
        except Exception as e:
            # Handle any other unexpected errors
            raise ValueError(f"An unexpected error occurred: {e}")
    

    def get_analysis_data(self) -> Dict[str, Any]:
        """Returns a dictionary of the core analysis results."""
        return {
            "average_brightness": self.avg_brightness,
            "brightest_point": list(self.max_loc),
            "darkest_point": list(self.min_loc),
            "brightest_value": float(self.max_val),
            "darkest_value": float(self.min_val)
        }

    def get_processed_image_with_highlights(self) -> np.ndarray:
        """
        Draws highlights on a *copy* of the original image and returns it.
        This is "non-destructive" to the original image data.
        """
        # Create a copy to avoid drawing on the original array
        img_with_highlights = self.img_color.copy()
        
        # Draw a red circle (BGR format) at the brightest location
        cv2.circle(img_with_highlights, self.max_loc, 10, (0, 0, 255), 2, cv2.LINE_AA)
        # Draw a blue circle at the darkest location
        cv2.circle(img_with_highlights, self.min_loc, 10, (255, 0, 0), 2, cv2.LINE_AA)
        
        return img_with_highlights

    @staticmethod
    def save_image(
        image_array: np.ndarray, 
        output_dir: str, 
        base_filename: str
    ) -> Tuple[str, str]:
        """
        Saves a NumPy image array to a file with a unique timestamp.
        Returns the (filename, full_save_path).
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize filename to avoid path traversal issues
        safe_filename = Path(base_filename).name
        filename = f"output_{timestamp}_{safe_filename}"
        
        save_path = os.path.join(output_dir, filename)
        
        try:
            cv2.imwrite(save_path, image_array)
            return filename, save_path
        except Exception as e:
            # Handle potential file system errors
            raise IOError(f"Could not save image to {save_path}: {e}")
