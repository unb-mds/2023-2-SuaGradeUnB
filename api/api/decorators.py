from django.core.cache import cache
from api.models import cache_error_msg
import functools


def handle_cache_before_delete(query_func: callable) -> callable:

    @functools.wraps(query_func)
    def wrapper(*args, **kwargs):
        queryset = query_func(*args, **kwargs)

        try:
            for query in queryset:
                cache_key = query.get_cache_key()
                cache.delete(cache_key)
        except: # pragma: no cover
            raise ValueError(cache_error_msg)
        else:
            queryset.delete()

    return wrapper
