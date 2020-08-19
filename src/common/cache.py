from .. import cache


class Cache:
    @classmethod
    def get(cls, key):
        return cache.cache.get(key)

    @classmethod
    def has(cls, key):
        return cache.cache.has(key)

    @classmethod
    def set(cls, key, val, timeout=30):
        return cache.cache.set(key, val, timeout)

    @classmethod
    def delete(cls, key):
        return cache.cache.delete(key)

    @classmethod
    def clear(cls):
        return cache.cache.clear()

    @classmethod
    def unmemoize(cls, f, **kwargs):
        return cache.delete_memoized(f, **kwargs)
