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
    DIGITAL_INPUT_VALUE = 2
    ANALOG_INPUT_VALUE = 20


__SET_DIGITAL_INPUT_STRUCT__ = struct.Struct('<ccc')


class CANCarry:
    def __init__(self, can_id: int):
        self.can_id = can_id
        self.__can: wpilib.CAN = wpilib.CAN(self.can_id)

        self.__last_digital_flags = 0b0

    def set_digital_input(self, sensor_id: int, pin: int):
        buff = bytearray(8)
        __SET_DIGITAL_INPUT_STRUCT__.pack_into(buff, 0, DeviceType.DIGITAL_INPUT, sensor_id, pin)

        self.__can.writePacket(buff, ApiID.SET_SENSOR)

    def get_digital_input(self, sensor_id: int) -> 'CANDigitalInput':
        return CANDigitalInput(self, sensor_id)

    def get_analog_input(self, sensor_id: int) -> 'CANAnalogInput':
        return CANAnalogInput(self, sensor_id)

    def __get_digital_flags__(self) -> int:
        data = wpilib.CANData()
        if self.__can.readPacketNew(ApiID.DIGITAL_INPUT_VALUE, data):
            self.__last_digital_flags = int.from_bytes(data.data, 'little')

        return self.__last_digital_flags

    def __get_analog__(self, sensor_id, last_val: int) -> int:
        data = wpilib.CANData()
        if self.__can.readPacketNew(ApiID.DIGITAL_INPUT_VALUE + sensor_id, data):
            return int.from_bytes(data.data, 'little')

        return last_val


class CANDigitalInput:
    def __init__(self, can_carry: CANCarry, sensor_id):
        self.__can_carry = can_carry
        self.sensor_id = sensor_id

    def get(self) -> bool:
        digital_flags = self.__can_carry.__get_digital_flags__()
        return (digital_flags << (63 - self.sensor_id)) < 0


class CANAnalogInput:
    def __init__(self, can_carry: CANCarry, sensor_id):
        self.__can_carry = can_carry
        self.sensor_id = sensor_id

        self.__last_val = 0

    def get(self) -> float:
        self.__last_val = self.__can_carry.__get_analog__(self.sensor_id, self.__last_val)
        return self.__last_val / 1023.

