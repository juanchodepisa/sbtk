from .misc import id_function
from .dictionaries import subdict
import json

# MAIN OBJECT

class Serializer(object):

    def __init__(self, object_type, parser, unparser):
        # parser and unparser must do the transformations between
        # the object and serializable built in types
        self.__type = object_type
        self.__parser = parser
        self.__unparser = unparser
        
    @property
    def object_type(self):
        return self.__type
        
    def parse(self, obj):
        # Unpythonic and ugly. Get over it
        if isinstance(obj, self.__type):
            builtin_obj = self.__parser(obj)
            result_dict ={'class'   : self.__type.__name__,
                          'module'  : self.__type.__module__,
                          'content' : builtin_obj}
            try:
                result_dict['metadata'] = obj.metadata
            except AttributeError as e:
                if hasattr(obj, 'metadata'):
                    raise e from None
            return json.dumps(result_dict)
        else:
            raise SerializationError(type(obj), self.__type)
        
    def unparse(self, serial_str, check_keys = {}):
        # Unpythonic and ugly. Get over it
        dic = json.loads(serial_str)
        tp = self.__type
        if dic['class'] == tp.__name__ and dic['module'] == tp.__module__:
            try:
                metadata = dic['metadata']
                with_metadata = True
            except KeyError:
                metadata = {}
                with_metadata = False
            
            if not subdict(check_keys, metadata):
                raise SerializationKeyError(metadata, check_keys)            
            elif with_metadata:
                return self.__unparser(dic['content'], metadata = metadata)
            else:
                return self.__unparser(dic['content'])
        else:
            raise SerializationError(tp.__module__+"."+tp.__name__, self.__type, parse = False)
    

###########################################################################











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
    