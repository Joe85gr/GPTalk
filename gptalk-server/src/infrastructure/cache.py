from logging import Logger

import redis

REDIS_HOST = '172.25.0.12'
REDIS_PORT = 6379
DEFAULT_TIMEOUT = 60 * 60 * 2


class Cache:
    def __init__(self, logger: Logger):
        self.logger = logger

    def GetFromCache(self, key: str):
        self.logger.info(f"Redis host: {REDIS_HOST}")
        self.logger.info(f"Redis port: {REDIS_PORT}")
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=2) as r:
            try:
                ping = r.ping()
                if ping is True:
                    return r.get(key)
                else:
                    self.logger.error("Cannot ping redis.")
            except Exception as e:
                self.logger.error("Unknown error with redis", e)
            return None

    def SetCache(self, key: str, value: str, timeout: int = DEFAULT_TIMEOUT):
        with redis.Redis(host=REDIS_HOST, socket_timeout=2) as r:
            try:
                ping = r.ping()
                if ping is True:
                    cached = r.setex(key, timeout, value)
                    return cached
                else:
                    self.logger.error("Cannot ping redis.")
            except Exception as e:
                self.logger.error("Unknown error with redis.", e)

        return False
