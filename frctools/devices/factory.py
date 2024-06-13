from enum import Enum
from frctools import WPI_CANSparkMax, WPI_TalonFX


import wpilib


BUILTIN_FACTORIES = []


class DeviceType(str, Enum):
    DIGITAL_INPUT = 'digital_input'
    DIGITAL_OUTPUT = 'digital_output'
    ENCODER = 'encoder'
    ANALOG_INPUT = 'analog_input'
    ANALOG_OUTPUT = 'analog_output'
    ANALOG_ENCODER = 'analog_encoder'
    DUTY_CYCLE_ENCODER = 'duty_cycle_encoder'
    CAN_SPARK_MAX = 'can_spark_max'
    TALON_FX = 'talon_fx'


class DeviceFactory:
    def __init__(self, device_type: str):
        self.__type = device_type

    @property
    def type(self):
        return self.__type

    def create_device(self, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        return self.create_device(*args, **kwargs)


class DigitalInputFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.DIGITAL_INPUT)

    def create_device(self, channel: int):
        return wpilib.DigitalInput(channel)


class DigitalOutputFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.DIGITAL_OUTPUT)

    def create_device(self, channel: int):
        return wpilib.DigitalOutput(channel)


class EncoderFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.ENCODER)

    def create_device(self, channel_a: int, channel_b: int, channel_index: int = None, reverse: bool = False):
        encoder = wpilib.Encoder(channel_a, channel_b, reverse)

        if channel_index is not None:
            encoder.setIndexSource(channel_index, wpilib.Encoder.IndexingType.kResetWhileHigh)

        return encoder


class AnalogInputFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.ANALOG_INPUT)

    def create_device(self, channel: int):
        return wpilib.AnalogInput(channel)


class AnalogOutputFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.ANALOG_OUTPUT)

    def create_device(self, channel: int):
        return wpilib.AnalogOutput(channel)


class AnalogEncoderFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.ANALOG_ENCODER)

    def create_device(self, channel: int):
        return wpilib.AnalogEncoder(channel)


class DutyCycleEncoderFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.DUTY_CYCLE_ENCODER)

    def create_device(self, channel: int):
        return wpilib.DutyCycleEncoder(channel)


class CANSparkMaxFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.CAN_SPARK_MAX)

    def create_device(self, can_id: int, brushless: bool, brake: bool = False, inverted: bool = False):
        return WPI_CANSparkMax(can_id, brushless, brake, inverted)


class TalonFXFactory(DeviceFactory):
    def __init__(self):
        super().__init__(DeviceType.TALON_FX)

    def create_device(self, can_id: int, brake: bool = False, inverted: bool = False):
        return WPI_TalonFX(can_id, brake, inverted)


BUILTIN_FACTORIES.append(DigitalInputFactory())
BUILTIN_FACTORIES.append(DigitalOutputFactory())
BUILTIN_FACTORIES.append(EncoderFactory())
BUILTIN_FACTORIES.append(AnalogInputFactory())
BUILTIN_FACTORIES.append(AnalogOutputFactory())
BUILTIN_FACTORIES.append(AnalogEncoderFactory())
BUILTIN_FACTORIES.append(DutyCycleEncoderFactory())
BUILTIN_FACTORIES.append(CANSparkMaxFactory())
BUILTIN_FACTORIES.append(TalonFXFactory())
