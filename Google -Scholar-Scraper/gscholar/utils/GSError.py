class GSException(BaseException):
    pass


class GSInvalidCacheException (GSException):
    def __init__(self, cache_object):
        self.cache_object = cache_object

# End of file
