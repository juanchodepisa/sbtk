from abc import ABCMeta, abstractmethod
from .misc import id_function
from .dictionaries import subdict

# MAIN OBJECT

class Serializer(object, metaclass = ABCMeta):
# pseudo abstract class

    def __init__(self, object_type, parser, unparser):
        # parser and unparser must do the transformations between
        # the object and serializable built in types
        self.__type = object_type
        self.__parser = parser
        self.__unparser = unparser
        
    @property
    def object_type(self):
        return self.__type
        
    @property
    @abstractmethod
    def loader(self):
        ...
        
    @property
    @abstractmethod
    def dumper(self):
        ...
        
    def parse(self, obj):
        # Unpythonic and ugly. Get over it
        if isinstance(obj, self.__type):
            builtin_obj = self.__parser(obj)
            result_dict ={
                '__class__'   : self.__type.__name__,
                '__module__'  : self.__type.__module__,
                '__comments__': "SBTK custom Python object",
                '__object__' : builtin_obj}
            try:
                result_dict['__metadata__'] = obj.__formatted_metadata__
            except AttributeError as e:
                if hasattr(obj, '__metadata__'):
                    raise e from None
            return self.dumper(result_dict)
        else:
            raise SerializationError(type(obj), self.__type)
        
    def unparse(self, serial_str, check_keys = {}):
        # Unpythonic and ugly. Get over it
        dic = self.loader(serial_str)
        tp = self.__type
        if dic['__class__'] == tp.__name__ and dic['__module__'] == tp.__module__:
            try:
                metadata = dic['__metadata__']
                with_metadata = True
            except KeyError:
                metadata = {}
                with_metadata = False
            
            if not subdict(check_keys, metadata):
                raise SerializationKeyError(metadata, check_keys)            
            elif with_metadata:
                return self.__unparser(dic['__object__'], metadata = metadata)
            else:
                return self.__unparser(dic['__object__'])
        else:
            raise SerializationError(tp.__module__+"."+tp.__name__, self.__type, parse = False)
    

###########################################################################

class JSONSerializer (Serializer):
    from json import loads as loader, dumps as dumper
    from functools import partial as __partial
    
    loader = staticmethod(loader)
    dumper = staticmethod(__partial(dumper, sort_keys=True, indent=4))
    
    







############################################################################

class SerializationError(Exception):
    def __init__(self, value, expected, parse = True):
        self.__parse = parse
        self.__expected = expected
        self.__value = value
        super().__init__(self.__str__())
    
    @property
    def value(self):
        return self.__value
        
    @property
    def expected(self):
        return self.__expected
        
    @property
    def parse(self):
        return self.__parse
        
        
    def __str__(self):
        if self.__parse:
            return "Parse: resulting object has type {v.__module__}.{v.__name__}; expected type: {et.__module__}.{et.__name__}".format(v = self.__value, et = self.__expected)
        else:
            return "Unparse: serialized objects indicates type {v}; expected type: {et.__module__}.{et.__name__}".format(v = self.__value, et = self.__expected)

class SerializationKeyError(SerializationError):
    def __init__(self, value, expected):
        super().__init__(value, expected, False)
        
    def __str__(self):
        return "Unparse: Failed to validate the keys. Keys = {ex}; Metadata = {v}".format(v = self.__value, ex = self.__expected)
    