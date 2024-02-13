import threading

from typing import Tuple


class CameraNotRunningError(Exception):
    def __init__(self, cam_name: str = 'cam'):
        super().__init__(f'{cam_name} is not running')


class BaseCameraThread:
    def __init__(self):
        self.__frame = None
        self.__frame_id = -1

        self.__running = False

    def start(self):
        if not self.__running:
            self.__running = True

            t = threading.Thread(target=self.__loop__, daemon=True)
            t.start()
        else:
            raise RuntimeError("Camera thread is already running")

    def stop(self):
        if self.__running:
            self.__running = False
        else:
            raise RuntimeError("Camera thread is not running")

    def __loop__(self):
        pass

    def get_frame_generator(self):
        last_frame_id = -1
        self.__running = True
        while self.__running:
            if last_frame_id == self.__frame_id:
                yield None
                continue

            last_frame_id = self.__frame_id
            yield self.__frame_id, self.__frame

    @property
    def is_running(self):
        return self.__running

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, frame):
        self.__frame = frame

    @property
    def frame_id(self):
        return self.__frame_id

    @frame_id.setter
    def frame_id(self, frame_id):
        self.__frame_id = frame_id


try:
    import os
    import cv2 as cv

    try:
        from picamera2 import Picamera2

        class Picamera2Wrapper:
            def __init__(self, device_id: int = 0):
                self.picam2 = Picamera2(device_id)

                config = self.picam2.create_preview_configuration(main={'size': (1456, 1088), 'format': 'RGB888'})
                self.picam2.configure(config)
                self.picam2.start()

            def read(self):
                try:
                    frame = self.picam2.capture_array('main')
                    return True, frame
                except Exception as e:
                    print(e)

                return False, None

            def release(self):
                self.picam2.stop()
    except ImportError:
        class Picamera2Wrapper:
            def __init__(self, *args, **kwargs):
                raise ImportError("picamera2 is not installed")


    class CameraCalibrator:
        def __init__(self, imgs: list):
            self.__imgs = imgs
            self.__win = None
            self.__img_label = None

        def calibrate(self):
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.__imgs, (9, 6), None, None)
            return mtx, dist

        @staticmethod
        def create_from_folder(folder: str):
            imgs = []
            for file in os.listdir(folder):
                if file.endswith('.jpg') or file.endswith('.png'):
                    imgs.append(cv.imread(f'{folder}/{file}'))
            return CameraCalibrator(imgs)


    class CameraThread(BaseCameraThread):
        def __init__(self, device_constructor):
            super().__init__()

            self.__device_constructor = device_constructor

        def __loop__(self):
            cap = self.__device_constructor()

            try:
                while self.is_running:
                    ret, frame = cap.read()
                    if ret:
                        self.frame = frame
                        self.frame_id += 1
                    else:
                        break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print(e)
            finally:
                cap.release()
                self.stop()

        @staticmethod
        def create_opencv(device_id: int = 0, resolution: Tuple[int, int] = (640, 480)):
            def cv_constructor():
                cap = cv.VideoCapture(device_id)
                cap.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
                cap.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])
                return cap

            return CameraThread(cv_constructor)

        @staticmethod
        def create_picamera(device_id: int = 0, resolution: Tuple[int, int] = (640, 480)):
            def picamera_constructor():
                cap = Picamera2Wrapper(device_id)
                return cap

            return CameraThread(picamera_constructor)

    class NetworkCameraThread(BaseCameraThread):
        def __init__(self):
            super().__init__()
        
        def __loop__(self):
            pass

except ImportError:
    class CameraCalibrator:
        def __init__(self, *args, **kwargs):
            raise ImportError("OpenCV is not installed")

    class CameraThread:
        def __init__(self, *args, **kwargs):
            raise ImportError("OpenCV is not installed")


    class NetworkCameraThread:
        def __init__(self, *args, **kwargs):
            raise ImportError("OpenCV is not installed")
