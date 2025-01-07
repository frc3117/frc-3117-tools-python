from .loader import ResourcesLoader
from frctools.frcmath import Vector2

import json


class TopViewResource:
    def __init__(self, name: str):
        with open(ResourcesLoader.get_resource_path(f'topview/{name}_meta.json'), 'r') as f:
            meta = json.load(f)

        field_meta = meta['field']

        self.field_min = Vector2(field_meta['min']['x'], field_meta['min']['y'])
        self.field_max = Vector2(field_meta['max']['x'], field_meta['max']['y'])
        self.field_size = Vector2(field_meta['size']['x'], field_meta['size']['y'])

        self.__img_path = ResourcesLoader.get_resource_path(f'topview/{name}.png')