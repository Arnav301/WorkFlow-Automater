# backend/app/services/vision.py
import cv2
import numpy as np
import pytesseract
from typing import List, Dict, Any
import easyocr

class UIVisionService:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])  # Initialize EasyOCR for better text detection
    
    def find_ui_elements(self, screenshot_path: str) -> List[Dict[str, Any]]:
        """Detect UI elements in a screenshot."""
        img = cv2.imread(screenshot_path)
        if img is None:
            raise ValueError("Could not read the image")
            
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect buttons (simple thresholding for demo)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        elements = []
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 20:  # Filter small elements
                element_img = img[y:y+h, x:x+w]
                
                # Extract text using EasyOCR
                text_results = self.reader.readtext(element_img, detail=0)
                text = " ".join(text_results) if text_results else ""
                
                elements.append({
                    "id": f"element_{i}",
                    "type": "button" if text else "element",
                    "text": text,
                    "position": {"x": x, "y": y, "width": w, "height": h},
                    "screenshot": f"data:image/png;base64,{self.image_to_base64(element_img)}"
                })
        
        return elements
    
    def image_to_base64(self, image):
        """Convert image to base64 for frontend display"""
        _, buffer = cv2.imencode('.png', image)
        import base64
        return base64.b64encode(buffer).decode('utf-8')