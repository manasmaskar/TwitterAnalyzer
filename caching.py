class InMemoryCache:
    def __init__(self, max_size=100):
        self.cache = OrderedDict()
        self.max_size = max_size

    def set(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def get(self, key):
        value = self.cache.get(key)
        if value:
            self.cache.move_to_end(key)
        return value

    def clear(self):
        self.cache.clear()


    #persisting cache state and monitoring, maintainance --->
    cache = InMemoryCache(max_size=100)

    def get_user_data(user_id):
        cache_key = f"user_data:{user_id}"
        data = cache.get(cache_key)
    
        if data is None:  # Cache miss
            data = fetch_user_data_from_database(user_id)  # Implement this
            cache.set(cache_key, data)
        return data