from .. import cache


class Cache:
    @staticmethod
    def get(key):
        return cache.cache.get(key)

    @staticmethod
    def has(key):
        return cache.cache.has(key)

    @staticmethod
    def set(key, val, timeout=30):
        return cache.cache.set(key, val, timeout)

    @staticmethod
    def delete(key):
        return cache.cache.delete(key)

    @staticmethod
    def clear():
        return cache.cache.clear()

    @staticmethod
    def unmemoize(f, **kwargs):
        return cache.delete_memoized(f, **kwargs)
