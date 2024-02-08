import os


class ResourcesLoader:
    @staticmethod
    def get_resource_path(resource_name: str) -> str:
        return os.path.join(os.path.dirname(__file__), resource_name)
