from .outline_service import outlineService

class OutlineGetter:
    _instance = None

    @classmethod
    def get_instance(cls, api_url=None, cert_sha256=None):
        if cls._instance is None:
            if api_url is None or cert_sha256 is None:
                raise ValueError("Must supply api_url and cert_sha256 for the first instantiation")
            cls._instance = outlineService(api_url, cert_sha256)
        return cls._instance
