from frctools import RobotBase

import wpiutil


class Component(wpiutil.Sendable):
    @property
    def robot(self):
        return RobotBase.instance()

    def init_auto(self):
        pass

    def update_auto(self):
        pass

    def init_teleop(self):
        pass

    def update_teleop(self):
        pass

    def init(self):
        pass

    def update(self):
        pass

    def initSendable(self, builder: wpiutil.SendableBuilder):
        pass
