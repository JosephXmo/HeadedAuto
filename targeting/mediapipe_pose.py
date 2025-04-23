import cv2
import mediapipe as mp


def get_extractor():
    # MediaPipe model for pose detection
    pose = mp.solutions.pose.Pose()

    def extract_target_coordinates(frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            nose = results.pose_landmarks.landmark[0]
            h, w = frame.shape[:2]
            x, y = int(nose.x * w), int(nose.y * h)
            return x, y
        return None
    
    return extract_target_coordinates