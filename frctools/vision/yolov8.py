try:
    from .camera import CameraThread
    from ultralytics import YOLO

    import os

    class YOLOv8:
        def __init__(self, camera: CameraThread, model_path: str):
            self.__camera = camera
            self.__frame_gen = camera.get_frame_generator()
            self.__yolo = YOLO(model_path)

        def look_for_objects(self):
            frame = next(self.__frame_gen)
            if frame is None:
                return None

            frame_id, frame = frame
            print(frame_id)

            return self.detect(frame)

        def detect(self, frame):
            return self.__yolo(frame)

except ImportError:
    class YOLOv8:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Ultralytics need to be installed installed.")
