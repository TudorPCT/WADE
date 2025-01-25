from collections import OrderedDict
from datetime import datetime, UTC, timedelta


class CacheEntry:
    def __init__(self, data, creation_time, ttl=300):
        self.data = data
        self.creation_time = creation_time
        self.ttl = ttl


class TTL_LRU_Cache:
    def __init__(self, capacity=1000, default_ttl=300):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.default_ttl = default_ttl

    def _is_expired(self, entry):
        return datetime.now(UTC) > entry.creation_time + timedelta(seconds=entry.ttl)

    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if self._is_expired(entry):
                del self.cache[key]
                return None
            else:
                self.cache.move_to_end(key)
                return entry.data
        return None

    def set(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.default_ttl

        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)

        self.cache[key] = CacheEntry(value, datetime.now(UTC), ttl)

    def size(self):
        return len(self.cache)

    def clear(self):
        self.cache.clear()