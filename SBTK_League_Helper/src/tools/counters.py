class MultiCounter(dict):
    def __init__(self, *args, default=0, increment=1):
        self.__default=0
        self.__increment=1
        super(MultiCounter, self).__init__(*args)
    
    def __missing__(self, key):
        return self.__default
    
    def __call__(self, key):
        self[key] = self[key] + self.__increment