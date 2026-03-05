import os
import json
import time

CACHE_FILE = "spot_cache.json"
CACHE_TTL = 60  # 缓存60秒


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if time.time() - data["time"] > CACHE_TTL:
        return None

    return data["data"]


def save_cache(data):

    with open(CACHE_FILE, "w", encoding="utf-8") as f:

        json.dump({
            "time": time.time(),
            "data": data
        }, f)