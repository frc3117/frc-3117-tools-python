import threading


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
    import cv2 as cv

    class CameraThread(BaseCameraThread):
        def __init__(self, device_id: int = 0, resolution: tuple = (640, 480), color_mode: str = 'rgb'):
            super().__init__()

            self.__device_id = device_id
            self.__resolution = resolution
            self.__color_mode = color_mode

        def __loop__(self):
            cap = cv.VideoCapture(self.__device_id)

            try:
                #cap.set(cv.CAP_PROP_FRAME_WIDTH, self.__resolution[0])
                #cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.__resolution[1])
                #cap.set(cv.CAP_PROP_MODE, self.__get_color_mode__())

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

        def __get_color_mode__(self):
            if self.__color_mode == 'rgb':
                return cv.COLOR_BGR2RGB
            elif self.__color_mode == 'hsv':
                return cv.CAP_MODE_HSV
            elif self.__color_mode == 'gray':
                return cv.CAP_MODE_GRAY

    class NetworkCameraThread(BaseCameraThread):
        def __init__(self):
            super().__init__()
        
        def __loop__(self):
            pass

except ImportError:
    class CameraThread:
        def __init__(self, *args, **kwargs):
            raise ImportError("OpenCV is not installed")


    class NetworkCameraThread:
        def __init__(self, *args, **kwargs):
            raise ImportError("OpenCV is not installed")
