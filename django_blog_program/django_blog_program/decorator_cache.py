import functools
import time
from collections import OrderedDict

CACHE = {}

def cache_it(max_size=1024, expire_time=60):
    CACHE = LRUCacheDict(max_size, expire_time)
    def  wrapper(func):
        @functools.wraps(func)
        def inner (*args, **kwargs):
            # cache_key = f'{func.__name__}_{args}_{kwargs}'
            cache_key = repr(*args, **kwargs)
            if cache_key in CACHE:
                return CACHE[cache_key]
            result = func(*args, **kwargs)
            CACHE[cache_key] = result
            return result
        return inner

class LRUCacheDict:
    def __init__(self, max_size=1024, expire_time=60):
        """最大容量1024， 过期时间60s"""
        self.max_size = max_size
        self .expire_time = expire_time

        self._cache = {}
        self._access_record = OrderedDict()
        self._expire_record = OrderedDict()

    def __setitem__(self, key, value):
        now = int(time.time())
        self.__delete__(key)

        self._cache[key] = value
        self._access_record[key] = now
        self._expire_record[key] = now + self.expire_time

        self.cleanup()

    def __getitem__(self, key):
        now =  int(time.time())
        del self._access_record[key]
        self._access_record[key] = now
        self.cleanup()
        return self._cache[key]

    def __delete__(self, key):
        if key in self._cache:
            del self._cache[key]
            del self._access_record[key]
            del self._expire_record[key]
        pass

    def cleanup(self):
        if self.expire_time is None:
            return None

        pending_delete_key = []
        now = int(time.time())
        for k, v in self._expire_record.items():
            if v < now:
                 pending_delete_key.append(k)

        for k in pending_delete_key:
            self.__delete__(k)

        while len(self._cache) > self.max_size:
            for k in self._access_record:
                self.__delete__(k)
                break





