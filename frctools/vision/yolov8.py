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

            self.__prev_frame_id = 0
            self.__prev_frame = None
            self.__prev_result = None

        def look_for_objects(self):
            frame = next(self.__frame_gen)
            if frame is None:
                return None

            frame_id, frame = frame
            if frame_id != self.__prev_frame_id:
                self.__prev_frame_id = frame_id
                self.__prev_frame = frame
                self.__prev_result = self.detect(frame)

            return self.__prev_frame_id, self.__prev_frame, self.__prev_result

        def detect(self, frame):
            return self.__yolo(frame, verbose=False)

        def get_cls_name(self, cls: int):
            return self.__names[cls]

except ImportError:
    class YOLOv8:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Ultralytics need to be installed installed.")
