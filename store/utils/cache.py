from django.core.cache import cache 
def get_cache(key):
    return cache.get(key)
def set_cache(key,data,timeout=300):
    cache.set(key,data,timeout)
    
def delete_cache(key):
    cache.delete(key)