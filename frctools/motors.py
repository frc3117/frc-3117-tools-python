class MotorGroup:
    def __init__(self, positives=None, negatives=None):
        self.positives = [] if positives is None else positives
        self.negatives = [] if negatives is None else negatives

    def set(self, value):
        for pos in self.positives:
            pos.set(value)

        for neg in self.negatives:
            neg.set(-value)


try:
    from rev import CANSparkMax

    class WPI_CANSparkMax(CANSparkMax):
        def __init__(self, can_id: int, brushless: bool, brake: bool = False, inverted: bool = False):
            super().__init__(can_id, self.__motor_type_from_bool__(brushless))

            self.__encoder = self.getEncoder()

            self.setIdleMode(self.__brake_from_bool__(brake))
            self.setInverted(inverted)

        def get(self) -> float:
            return self.__encoder.getVelocity()

        def set_voltage(self, voltage: float):
            self.setVoltage(voltage)

        def get_voltage(self) -> float:
            return self.getBusVoltage()

        def set_brake(self, brake: bool):
            self.setIdleMode(self.__brake_from_bool__(brake))

        def get_brake(self) -> bool:
            return self.getIdleMode() == CANSparkMax.IdleMode.kBrake

        def set_inverted(self, inverted: bool):
            self.setInverted(inverted)

        def get_inverted(self) -> bool:
            return self.getInverted()

        @staticmethod
        def __motor_type_from_bool__(b: bool) -> CANSparkMax.MotorType:
            return CANSparkMax.MotorType.kBrushless if b else CANSparkMax.MotorType.kBrushed

        @staticmethod
        def __brake_from_bool__(b: bool) -> CANSparkMax.IdleMode:
            return CANSparkMax.IdleMode.kBrake if b else CANSparkMax.IdleMode.kCoast
except ImportError:
    class WPI_CANSparkMax:
        def __init__(self, can_id: int, brushless: bool, brake: bool = False, inverted: bool = False):
            raise NotImplementedError("rev library is not installed")


try:
    from phoenix6.hardware import TalonFX
    from phoenix6.controls import VelocityDutyCycle, VoltageOut
    from phoenix6.configs import TalonFXConfiguration
    from phoenix6.configs.talon_fx_configs import NeutralModeValue, InvertedValue


    class WPI_TalonFX(TalonFX):
        def __init__(self, can_id: int, brake: bool = False, inverted: bool = False):
            super().__init__(can_id)

            self.config = TalonFXConfiguration()
            self.configurator.refresh(self.config)

            self.config.motor_output.neutral_mode = WPI_TalonFX.__brake_from_bool__(brake)
            self.config.inverted = WPI_TalonFX.__inverted_from_bool__(inverted)

            self.__duty_cycle_out = VelocityDutyCycle(0, enable_foc=False)
            self.__voltage_out = VoltageOut(0, enable_foc=False)

            self.configurator.apply(self.config)
            self.set_control(self.__voltage_out)

        def set(self, value: float):
            self.set_control(self.__duty_cycle_out.with_velocity(value))

        def get(self) -> float:
            return self.get_velocity().value

        def set_voltage(self, voltage: float):
            self.set_control(self.__voltage_out.with_output(voltage))

        def get_voltage(self) -> float:
            return self.get_motor_voltage().value

        def set_brake(self, brake: bool):
            self.configurator.apply(self.config.with_motor_output(self.config.motor_output.with_neutral_mode(WPI_TalonFX.__brake_from_bool__(brake))))

        def get_brake(self) -> bool:
            return self.config.motor_output.neutral_mode == NeutralModeValue.BRAKE

        def set_inverted(self, inverted: bool):
            self.configurator.apply(self.config.with_motor_output(self.config.motor_output.with_inverted(WPI_TalonFX.__inverted_from_bool__(inverted))))

        def get_inverted(self) -> bool:
            return self.config.motor_output.inverted == InvertedValue.COUNTER_CLOCKWISE_POSITIVE

        @staticmethod
        def __brake_from_bool__(b):
            return NeutralModeValue.BRAKE if b else NeutralModeValue.COAST

        @staticmethod
        def __inverted_from_bool__(b):
            return InvertedValue.COUNTER_CLOCKWISE_POSITIVE if b else InvertedValue.CLOCKWISE_POSITIVE
except ImportError:
    class WPI_TalonFX:
        def __init__(self, can_id: int, brake: bool = False, inverted: bool = False):
            raise NotImplementedError("phoenix6 library is not installed")


