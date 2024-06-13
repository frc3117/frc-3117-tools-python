from .factory import DeviceFactory, BUILTIN_FACTORIES

import json


class DevicesManager:
    def __init__(self, use_builtin_factories: bool = True):
        self.__factories = {}
        self.__devices = {}

        if use_builtin_factories:
            for factory in BUILTIN_FACTORIES:
                self.add_factory(factory)

    def load_devices(self, devices):
        for dev in devices:
            dev_name = dev['name']
            dev_type = dev['type']
            dev_params = dev['params']

            if dev_type not in self.__factories:
                raise ValueError(f'Unknown device type: {dev_type}')

            self.__devices[dev_name] = self.__factories[dev_type](**dev_params)

    def load_devices_json(self, json_dict: str = None, json_path: str = None):
        if json_dict is not None:
            self.load_devices(json_dict)
        elif json_path is not None:
            with open(json_path, 'r') as file:
                self.load_devices(json.load(file))

    def add_factory(self, dev_factory: DeviceFactory):
        self.__factories[dev_factory.type] = dev_factory

    def get_device(self, device_name: str):
        if device_name not in self.__devices:
            raise ValueError(f'Unknown device: {device_name}')

        return self.__devices[device_name]
