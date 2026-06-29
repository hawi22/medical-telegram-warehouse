import os
import pandas as pd
from ultralytics import YOLO
from glob import glob

# Load YOLOv8 nano model (it will download automatically)
model = YOLO('yolov8n.pt')

def classify_image(detections):
    classes = [d['class'] for d in detections]
    
    # Classification Logic
    has_person = 'person' in classes
    has_product = any(item in classes for item in ['bottle', 'cup', 'vial', 'bowl', 'box'])

    if has_person and has_product:
        return 'promotional'
    elif has_product:
        return 'product_display'
    elif has_person:
        return 'lifestyle'
    else:
        return 'other'

def run_detection(image_root):
    results_list = []
    
    # Find all images in data/raw/images/{channel}/{id}.jpg
    image_paths = glob(os.path.join(image_root, "**", "*.jpg"), recursive=True)
    
    print(f"Found {len(image_paths)} images. Running detection...")

    for path in image_paths:
        # Extract metadata from path
        parts = os.path.normpath(path).split(os.sep)
        channel_name = parts[-2]
        message_id = parts[-1].replace(".jpg", "")

        # Run YOLO
        results = model(path, verbose=False)
        
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    'class': model.names[int(box.cls)],
                    'confidence': float(box.conf)
                })
        
        category = classify_image(detections)
        
        results_list.append({
            'message_id': int(message_id),
            'channel_name': channel_name,
            'detected_objects': ",".join([d['class'] for d in detections]),
            'image_category': category
        })

    # Save to CSV for loading into DB
    df = pd.DataFrame(results_list)
    output_path = "data/yolo_detections.csv"
    df.to_csv(output_path, index=False)
    print(f"Detections complete. Results saved to {output_path}")

if __name__ == "__main__":
    run_detection("data/raw/images")