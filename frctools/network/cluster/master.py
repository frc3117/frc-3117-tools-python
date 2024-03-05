from typing import List
from socketserver import TCPServer, UDPServer


class ClusterMasterChannel:
    pass


class TCPClusterMasterChannel(ClusterMasterChannel):
    pass


class UDPClusterMasterChannel(ClusterMasterChannel):
    pass


class ClusterMaster:
    def __init__(self, channels: List[ClusterMasterChannel]):
        self.__coroutine = None

    def start(self):
        if self.__coroutine is None:
            self.__coroutine = self.__loop__()

    def stop(self):
        if self.__coroutine is not None:
            self.__coroutine = None

    def get_coroutine(self):
        pass

    def update(self):
        try:
            next(self.__coroutine)
        except StopIteration:
            self.stop()

    def __loop__(self):
        yield None

