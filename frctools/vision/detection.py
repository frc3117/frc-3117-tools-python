from frctools import HarfangsDashboard


class ObjectDetection:
    def __init__(self, name):
        self.__detection_table = HarfangsDashboard.instance().get_table(f'detection/{name}')


    def update_nt(self):
        pass
