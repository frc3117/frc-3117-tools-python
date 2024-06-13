from typing import List, Dict
from socketserver import TCPServer, UDPServer
from .shared import BuiltinsMessageType, ClusterConnection, TCPConnection

import socket


class ClusterMasterChannel:
    pass


class MasterChannelConnection:
    def send(self, data):
        pass

    def receive(self):
        pass


class RemoteClient:
    def __init__(self, name: str):
        self.name = name
        self.__channels = {}

    def add_channel(self, name: str, connection: ClusterConnection):
        self.__channels[name] = connection

    def send(self, channel_name: str, data):
        self.__channels[channel_name].send(data)


class TCPClusterMasterChannel(ClusterMasterChannel):
    def __init__(self, name: str, port: int, host: str = '0.0.0.0'):
        self.__name = name
        self.__port = port
        self.__host = host

        self.__socket = None
        self.__connections: List[ClusterConnection] = []
        self.__registred_connection: Dict[str, ClusterConnection] = {}
        self.__registred_callback = []

        self.__is_running = False

    def start(self):
        if not self.__is_running:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__host, self.__port))
            self.__socket.setblocking(False)

            self.__is_running = False

    def stop(self):
        if self.__is_running:
            self.__socket.close()
            self.__is_running = False

    def get_channel_name(self) -> str:
        return self.__name

    def on_registred_callback(self, callback):
        self.__registred_callback.append(callback)

    def __accept__(self):
        try:
            while True:
                conn, addr = self.__socket.accept()
                tcp_conn = TCPConnection(conn)
                self.__connections.append(tcp_conn)
        except:
            pass

    def __receive__(self):
        for conn in self.__connections:
            data = conn.receive()
            if data is None:
                continue

            message_type = data.get_message_type()
            if message_type == BuiltinsMessageType.REGISTER:
                name = data.read_string()
                self.__registred_connection[name] = conn
                for callback in self.__registred_callback:
                    callback(self, name, conn)
            elif message_type == BuiltinsMessageType.PRINT:
                text = data.read_string()
                print(text)


class UDPClusterMasterChannel(ClusterMasterChannel, UDPServer):
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

