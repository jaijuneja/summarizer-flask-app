from flask.ext.cache import Cache

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 24*60*60
})