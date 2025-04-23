def get_extractor(model):
    if model == "mediapipe":
        from .mediapipe_pose import get_extractor as get_mediapipe
        return get_mediapipe()
    elif model == "yolov8":
        from .yolov8_pose import get_extractor as get_yolov8
        return get_yolov8()
    else:
        raise ValueError(f"Unsupported model: {model}")