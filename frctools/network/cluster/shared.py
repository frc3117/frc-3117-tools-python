from enum import Enum


class BuiltinsMessageType(Enum):
    HEARTBEAT = 0
    REGISTER = 1
    PRINT = 2


class MessageBuffer:
    def __init__(self, buffer=None):
        self.__pointer = 0

        if buffer is None:
            self.__buffer = bytearray(4)
            self.__message_type = None
        else:
            self.__buffer = buffer
            self.__message_type = self.read_int(length=4, signed=False)

    def set_message_type(self, message_type: int):
        self.__message_type = message_type
        self.__buffer[0:4] = message_type.to_bytes(length=4, byteorder='big', signed=True)

    def get_message_type(self) -> int:
        return self.__message_type

    def read_bytes(self, length: int) -> bytearray:
        buff = self.__buffer[self.__pointer: self.__pointer + length]
        self.__pointer += length

        return buff

    def add_bytes(self, data: bytearray):
        self.__buffer += data
        return self

    def read_int(self, length: int, signed: bool = True) -> int:
        return int.from_bytes(self.read_bytes(length), byteorder='big', signed=signed)

    def add_int(self, data: int, length: int = 4, signed: bool = True):
        self.add_bytes(bytearray(data.to_bytes(length=length, byteorder='big', signed=signed)))
        return self

    def read_string(self, encoding: str = 'utf8'):
        str_length = self.read_int(4, False)
        return self.read_bytes(str_length).decode(encoding)

    def add_string(self, data: str, encoding: str = 'utf8'):
        self.add_int(len(data), 4, False)
        self.add_bytes(bytearray(data.encode(encoding)))
        return self

    def get_buffer(self, with_length: bool = True):
        if with_length:
            length = len(self.__buffer)
            return bytearray(length.to_bytes(length=4, byteorder='big', signed=False)) + self.__buffer

        return self.__buffer


class ClusterConnection:
    def send(self, message: MessageBuffer):
        pass

    def receive(self) -> MessageBuffer:
        pass


class TCPConnection(ClusterConnection):
    def __init__(self, tcp_connection):
        self.__conn = tcp_connection

        self.__current_bytes = bytearray()
        self.__byte_to_read = -1

    def send(self, message: MessageBuffer):
        buff = message.get_buffer()
        self.__conn.sendall(buff)

    def __recv__(self, length: int):
        try:
            return self.__conn.recv(length)
        except:
            return None

    def receive(self):
        if self.__byte_to_read == -1:
            out = self.__recv__(4)
            if out is None:
                return None

            self.__current_bytes = bytearray()
            self.__byte_to_read = int.from_bytes(out, byteorder='big', signed=False)

        out = self.__recv__(self.__byte_to_read)
        if out is None:
            return None

        self.__current_bytes += out
        self.__byte_to_read -= len(out)

        if self.__byte_to_read == 0:
            self.__byte_to_read = -1
            return MessageBuffer(buffer=self.__current_bytes)

        return None
