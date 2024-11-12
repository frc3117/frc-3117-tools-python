from typing import Tuple

try:
    from mjpeg_streamer import MjpegServer, Stream


    class MjpegStreamer:
        def __init__(self, host: str = '0.0.0.0', port: int = 8081):
            self.__server = MjpegServer(host, port)
            self.__streams = {}

        def create_stream(self, name: str, fps: int = 30, resolution: Tuple[int, int] = (1280, 720), quality: int = 50) -> Stream:
            if name in self.__streams:
                raise Exception('Stream with the same name already exist')

            # Create the stream
            stream = Stream(name, fps, resolution, quality)
            self.__streams[name] = stream

            # Stop the server if it is already running
            need_restart = False
            if self.__server.is_running():
                self.stop()
                need_restart = True

            # Add the stream to the server
            self.__server.add_stream(stream)

            # Start the server again if it was already running
            if need_restart:
                self.start()

            return stream

        def start(self):
            self.__server.start()

        def stop(self):
            self.__server.stop()
except ImportError:
    class MjpegStreamer:
        def __init__(self, *args, **kwargs):
            raise ImportError('mjpeg_streamer is not installed')