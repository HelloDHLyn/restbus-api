import urllib3


class HttpHelper(object):
    _pool = urllib3.PoolManager()

    @classmethod
    def pool(cls):
        return cls._pool
