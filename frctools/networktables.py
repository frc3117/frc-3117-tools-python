import ntcore


class HarfangsDashboardTable:
    pass


class HarfangsDashboard:
    __INSTANCE__: 'HarfangsDashboard' = None

    def __init__(self, nt: ntcore.NetworkTableInstance):
        self.__nt = nt

    @staticmethod
    def init_roborio():
        if HarfangsDashboard.__INSTANCE__ is None:
            nt = ntcore.NetworkTableInstance.getDefault()

            HarfangsDashboard.__INSTANCE__ = HarfangsDashboard(nt)
            return HarfangsDashboard.__INSTANCE__

        raise Exception('')

    @staticmethod
    def init_client(identity: str, hostname: str, version: int = 4) -> 'HarfangsDashboard':
        if HarfangsDashboard.__INSTANCE__ is None:
            nt = ntcore.NetworkTableInstance.getDefault()

            if version == 3:
                nt.startClient3(identity)
                nt.setServer(hostname, ntcore.NetworkTableInstance.kDefaultPort3)
            elif version == 4:
                nt.startClient4(identity)
                nt.setServer(hostname, ntcore.NetworkTableInstance.kDefaultPort4)
            else:
                raise Exception('')

            HarfangsDashboard.__INSTANCE__ = HarfangsDashboard(nt)
            return HarfangsDashboard.__INSTANCE__

        raise Exception('')

    @staticmethod
    def instance() -> 'HarfangsDashboard':
        return HarfangsDashboard.__INSTANCE__

    def get_table(self, key) -> ntcore.NetworkTable:
        return self.__nt.getTable(f'frc3117/{key}')

    def boolean_entry(self, key):
        pass
