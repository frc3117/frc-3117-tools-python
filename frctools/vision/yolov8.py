try:
    from .camera import CameraThread
    from ultralytics import YOLO

    import os

    class YOLOv8:
        def __init__(self, camera: CameraThread, model_path: str):
            self.__camera = camera
            self.__frame_gen = camera.get_frame_generator()
            self.__yolo = YOLO(model_path)

            self.__names = self.__yolo.names

        def look_for_objects(self):
            frame = next(self.__frame_gen)
            if frame is None:
                return None

            frame_id, frame = frame

            return self.detect(frame)

        def detect(self, frame):
            return self.__yolo(frame, verbose=False)

        def get_cls_name(self, cls: int):
            return self.__names[cls]

except ImportError:
    class YOLOv8:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Ultralytics need to be installed installed.")
