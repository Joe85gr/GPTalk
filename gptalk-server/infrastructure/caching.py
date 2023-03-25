import redis
from redis import TimeoutError as RedisTimeoutError

CACHE_TIMEOUT = 60 * 24
REDIS_HOST = '172.20.0.12'
REDIS_PORT = 6379


class Cache:
    def getFromCache(self, key: str):
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_timeout=1) as r:
            try:
                ping = r.ping()
                if ping is True:
                    return r.get(key)
                else:
                    return None
            except RedisTimeoutError:
                return None

    def setCache(self, key: str, value: str):
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0) as r:
            try:
                ping = r.ping()
                if ping is True:
                    return r.setex(key, CACHE_TIMEOUT, value)
                else:
                    return None
            except RedisTimeoutError:
                return None
