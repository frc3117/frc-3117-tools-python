from enum import Enum

import struct
import wpilib


class DeviceType(int, Enum):
    DIGITAL_INPUT = 0
    DIGITAL_OUTPUT = 1
    ANALOG_INPUT = 2
    ANALOG_OUTPUT = 3


class ApiID(int, Enum):
    SET_SENSOR = 0
    REMOVE_SENSOR = 1


__SET_DIGITAL_INPUT_STRUCT__ = struct.Struct('<ccc')


class CANCarry:
    def __init__(self, can_id: int):
        self.can_id = can_id
        self.__can: wpilib.CAN = wpilib.CAN(self.can_id)

    def set_digital_input(self, sensor_id: int, pin: int):
        buff = bytearray(8)
        __SET_DIGITAL_INPUT_STRUCT__.pack_into(buff, 0, DeviceType.DIGITAL_INPUT, sensor_id, pin)

        self.__can.writePacket(buff, ApiID.SET_SENSOR)


class CANDigitalInput:
    def __init__(self, can_carry: CANCarry, sensor_id):
        self.__can_carry = can_carry
        self.sensor_id = sensor_id

