from .counters import MultiCounter

class AdHocMarker(object):
    __counters = MultiCounter()
    def __init__(self, mark, scope=None):
        self.__id = (AdHocMarker.__counters[scope], scope)
        AdHocMarker.__counters(scope)
        self.mark = mark
        
    def check_scope(self, scope):
        return self.__id[1] is scope
        
    def __str__(self):
        return "\u00b6%s" % self.mark

    def __repr__(self):
        return "\u00b6%d:%s" % (self.__id[0], self.mark)
    
    def __call__(self, dict):
        return dict[self]