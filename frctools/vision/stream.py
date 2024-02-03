import threading


try:
    from cscore import CameraServer, CvSource

    class VideoStreamServer:
        def __init__(self, name: str):
            self.__name: str = name

            self.__is_running: bool = False

            self.__frame = None
            self.__frame_id: int = None
            self.__sent_frame_id: int = None

        def start(self, width: int, height: int):
            if not self.__is_running:
                self.__is_running = True

                t = threading.Thread(target=self.__server_thread__, args=(width, height), daemon=True)
                t.start()
            else:
                raise RuntimeError("Camera thread is already running")

        def stop(self):
            if self.__is_running:
                self.__is_running = False
            else:
                raise RuntimeError("Camera thread is not running")

        def __server_thread__(self, width: int, height: int):
            source = CameraServer.putVideo(self.__name, width, height)

            try:
                while self.__is_running:
                    if self.__frame_id != self.__sent_frame_id:
                        source.putFrame(self.__frame)
                        self.__sent_frame_id = self.__frame_id
            except Exception as e:
                print(e)
            finally:
                self.__is_running = False

        def put(self, frame, frame_id: int):
            self.__frame = frame
            self.__frame_id = frame_id

    class VideoStreamClient:
        def __init__(self):
            pass

        def start(self):
            pass

        def stop(self):
            pass

        def get(self):
            pass

except ImportError:
    class VideoStreamServer:
        def __init__(self, *args, **kwargs):
            raise ImportError('cv2 needs to be installed.')


    class VideoStreamClient:
        def __init__(self, *args, **kwargs):
            raise ImportError('cv2 needs to be installed.')