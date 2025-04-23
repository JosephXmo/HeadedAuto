import cv2
import torch
from ultralytics import YOLO


def get_extractor():
    # YOLOv8 model for human detection
    model = YOLO("yolov8n-pose.pt")
    # model = YOLO("yolov8s-pose.pt")
    # model = YOLO("yolov8m-pose.pt")
    # model = YOLO("yolov8l-pose.pt")
    # model = YOLO("yolov8x-pose.pt")
    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    print(f"[INFO] Using device: {device}")

    def extract_target_coordinates(frame):
        results = model.predict(source=frame, conf=0.3, iou=0.4, verbose=False, device=device)
        h, w = frame.shape[:2]

        # if results[0].keypoints.shape[0] > 0:       # Pick first body
        #     for person_keypoints in results[0].keypoints.data:
        #         if person_keypoints[0][4] > 0:
        #             nose_x, nose_y = person_keypoints[0][0].item(), person_keypoints[0][1].item()
        #             return nose_x, nose_y
        if results and results[0].keypoints.shape[1] > 0:
            keypoints = results[0].keypoints.xy  # shape: (num_persons, 17, 2)
            if keypoints.shape[0] > 0:
                # 取第一个检测到的人体的鼻尖关键点（COCO17 的 index 0）
                nose = keypoints[0][0]
                return int(nose[0]), int(nose[1])
        return None
    
    return extract_target_coordinates