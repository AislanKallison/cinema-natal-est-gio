# utils/redis_lock.py
import redis
from django.conf import settings
from contextlib import contextmanager
from time import sleep

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

@contextmanager
def seat_lock(seat_id: str, acquire_timeout=10, lock_timeout=30):
    lock_key = f"lock:seat:{seat_id}"
    start = time.time()
    while time.time() - start < acquire_timeout:
        if redis_client.set(lock_key, "locked", nx=True, ex=lock_timeout):
            try:
                yield
            finally:
                redis_client.delete(lock_key)
            return
        sleep(0.1)
    raise Exception("Não foi possível adquirir lock para o assento")