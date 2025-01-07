import os


__DIRNAME__ = os.path.dirname(__file__)


class ResourcesLoader:
    @staticmethod
    def get_resource_path(resource_name: str) -> str:
        return os.path.join(__DIRNAME__, resource_name)
