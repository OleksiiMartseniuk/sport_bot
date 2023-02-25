def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


def get_max_offset(count: int, limit: int) -> int:
    if not count % limit:
        return (int(count / limit) * limit) - limit
    return int(count / limit) * limit
