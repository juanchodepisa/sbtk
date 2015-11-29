# This comes directly from Leira's Project Euler utilities
# turns out the tool is actually too powerful for this purpose, so
# this is a simplified version

from functools import wraps


# The function must take only one parameter
class Simple_Dynamic_Memory():
        
    ############################
    ##     basic methods      ##
    ############################
    
    def __init__(self, function):
        self.__function = function
        self.__container = dict()
    
    def __del__(self):
        del self.__container
    
    
    ############################
    ##   emulation methods    ##
    ############################
    
    def __call__ (self, x):
        container = self.__container
        try:
            result = container[x]
        except KeyError:
            container[x] = result = self.__function(x)
        
        return result
        
    ############################
    ##     public methods     ##
    ############################
    
    def __reset_cache (self):
        self.__container = dict()
        
    cache = property(lambda self: self.__container, None, __reset_cache, "Dynamically stored memory.")
    
    
    ###########################

 
def simple_dynamic_memory(function):
    return wraps(function)(Simple_Dynamic_Memory(function))
