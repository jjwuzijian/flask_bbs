import memcache

cache = memcache.Client(['127.0.0.1:11211'],debug=True)

def set(key,value,timeout=600):
    return cache.set(key,value,timeout)

def delete(key):
    return cache.delete(key)
