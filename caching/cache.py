from flask_caching import Cache

def create_cache (app):
    cache = None
    try:
        app.config["CACHE_URL"] = app.config["CACHE_URL"] if "CACHE_URL" in app.config else "redis://127.0.0.1:6379"
        app.config["CACHE_HOST"]= app.config["CACHE_HOST"] if "CACHE_HOST" in app.config else "localhost"
        app.config["CACHE_PORT"]= app.config["CACHE_PORT"] if "CACHE_PORT" in app.config else 6379
        app.config["CACHE_DB"]= app.config["CACHE_DB"] if "CACHE_DB" in app.config else 0
        app.config["CACHE_DEFAULT_TIMEOUT"]= app.config["CACHE_DEFAULT_TIMEOUT"] if "CACHE_DEFAULT_TIMEOUT" in app.config else 86400
        app.config["CACHE_KEY_PREFIX"]= app.config["CACHE_KEY_PREFIX"] if "CACHE_KEY_PREFIX" in app.config else "fairhub-io#"

        cache = Cache(
            config={
                "CACHE_TYPE": "RedisCache",
                "CACHE_DEBUG": False,
                "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
                "CACHE_KEY_PREFIX": app.config["CACHE_KEY_PREFIX"],
                "CACHE_REDIS_HOST": app.config["CACHE_HOST"],
                "CACHE_REDIS_PORT": app.config["CACHE_PORT"],
                "CACHE_REDIS_DB": app.config["CACHE_DB"],
                "CACHE_REDIS_URL": app.config["CACHE_URL"],
            }
        )
    except:
        raise RuntimeError("Unable to instantiate cache!")
    return cache
