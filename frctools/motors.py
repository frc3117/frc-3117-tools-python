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
    from rev import SparkBase, SparkBaseConfig, SparkMax, SparkMaxConfig, SparkFlex, SparkFlexConfig


    def __motor_type_from_bool__(b: bool) -> SparkBase.MotorType:
        return SparkBase.MotorType.kBrushless if b else SparkBase.MotorType.kBrushed

    def __brake_from_bool__(b: bool) -> SparkBaseConfig.IdleMode:
        return SparkBaseConfig.IdleMode.kBrake if b else SparkBaseConfig.IdleMode.kCoast


    class WPI_CANSparkMax(SparkMax):
        def __init__(self, can_id: int, brushless: bool, brake: bool = False, inverted: bool = False):
            super().__init__(can_id, __motor_type_from_bool__(brushless))

            self.__encoder = self.getEncoder()

            self.__config = SparkMaxConfig()
            self.__config.setIdleMode(__brake_from_bool__(brake))
            self.__config.inverted(inverted)

        def get(self) -> float:
            return self.__encoder.getVelocity()

        def set_voltage(self, voltage: float):
            self.setVoltage(voltage)
        def get_voltage(self) -> float:
            return self.getBusVoltage()

        def set_brake(self, brake: bool):
            self.__config.setIdleMode(__brake_from_bool__(brake))
            self.configure(self.__config, SparkBase.ResetMode.kResetSafeParameters, SparkBase.PersistMode.kPersistParameters)
        def get_brake(self) -> bool:
            return self.configAccessor.getIdleMode() == SparkBase.IdleMode.kBrake

        def set_inverted(self, inverted: bool):
            self.__config.inverted(inverted)
            self.configure(self.__config, SparkBase.ResetMode.kResetSafeParameters, SparkBase.PersistMode.kPersistParameters)
        def get_inverted(self) -> bool:
            return self.configAccessor.getInverted()


    class WPI_CANSparkFlex(SparkFlex):
        def __init__(self, can_id: int, brushless: bool, brake: bool = False, inverted: bool = False):
            super().__init__(can_id, __motor_type_from_bool__(brushless))

            self.__encoder = self.getEncoder()

            self.__config = SparkFlexConfig()
            self.__config.setIdleMode(__brake_from_bool__(brake))
            self.__config.inverted(inverted)

        def get(self) -> float:
            return self.__encoder.getVelocity()

        def set_voltage(self, voltage: float):
            self.setVoltage(voltage)

        def get_voltage(self) -> float:
            return self.getBusVoltage()

        def set_brake(self, brake: bool):
            self.__config.setIdleMode(__brake_from_bool__(brake))
            self.configure(self.__config, SparkBase.ResetMode.kResetSafeParameters, SparkBase.PersistMode.kPersistParameters)

        def get_brake(self) -> bool:
            return self.configAccessor.getIdleMode() == SparkBase.IdleMode.kBrake

        def set_inverted(self, inverted: bool):
            self.__config.inverted(inverted)
            self.configure(self.__config, SparkBase.ResetMode.kResetSafeParameters, SparkBase.PersistMode.kPersistParameters)

        def get_inverted(self) -> bool:
            return self.configAccessor.getInverted()

except ImportError:
    class WPI_CANSparkMax:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("rev library is not installed")

    class WPI_CANSparkFlex:
        def __init__(self, *args, **kwargs):
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
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("phoenix6 library is not installed")


