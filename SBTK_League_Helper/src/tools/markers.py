from collections import Counter

class AdHocMarker(object):
    __counters = Counter()
    def __init__(self, mark, scope=None):
        self.__id = (AdHocMarker.__counters[scope], scope)
        AdHocMarker.__counters[scope] += 1
        self.__mark = mark
    
    @property
    def mark(self):
        return self.__mark
    
    @property
    def scope(self):
        return self.__id[1]
        
    def check_scope(self, scope):
        return self.__id[1] is scope
        
    def __str__(self):
        return "\u00b6{}".format(self.__mark)

    def __repr__(self):
        return "<{id[1]} \u00b6{id[0]}: {m}>".format(id = self.__id, m = self.__mark)
    
    def __call__(self, dict):
        return dict[self]