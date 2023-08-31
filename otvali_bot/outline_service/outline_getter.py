from .outline_service import outlineService

class OutlineGetter:
    _instance = None

    @classmethod
    def get_instance(cls, base_url=None):
        if cls._instance is None:
            if base_url is None:
                raise ValueError("Must supply api_url and cert_sha256 for the first instantiation")
            cls._instance = outlineService(base_url)
        return cls._instance
