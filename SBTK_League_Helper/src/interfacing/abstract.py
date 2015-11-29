from collections import UserDict
from datetime import datetime
from urllib.parse import quote, unquote
from os import path

from src.tools.date_time import utc, localtz
from src.tools.dynamic_programming import simple_dynamic_memory
from .exceptions import DataCorruptedError

class ServerElement(UserDict):
## This is a simple pseudo-abstract class
## to_builtin() and from_builtin() must be implemented in the subclasses
## this should transform the class object into built in types, for serializing
    def __init__(self, server, id, info, timestamp = None):
        if timestamp:
            self.__timestamp = timestamp
        else:
            # always normalize with UTC, otherwise nightmares ensue
            # represent the age of the info.
            self.__timestamp = datetime.now(tz = utc)
        self.__server = server
        self.__id = id
        super().__init__(info)
    
    ################
    ## PROPERTIES ##
    ## & METHODS  ##
    ################
    
    # Some of these exist to provide easy overrides
    
    @property
    def server(self):
        return self.__server
    
    @property
    def id(self):
        return self.__id
    
    @property
    def timestamp(self):
        return self.__timestamp
        
    @property
    def metadata(self):
        return dict(
            id = self.__id,
            server = self.__server.shortname,
            timestamp = self.__timestamp.isoformat())

    def filename(self, extension = "json"):
        return self.standard_filename(self.__server, self.__id, extension = extension)
    
    @classmethod
    def standard_filename(Class, server, id , extension = "json"):
        return "{server}-{cls.__name__}-{cls.__module__}-{safeid}.{ext}".format(
            server=server.shortname,
            cls=Class,
            safeid = quote(str(id), safe=""), 
            ext=extension)
    
    @staticmethod
    def get_keys(**kwargs):
        return {'id' : kwargs['id'], 'server' : kwargs['server'].shortname}
            
    ################
    ## SERIALIZER ##
    ##   OBJECT   ##
    ################
     
    @classmethod
    @simple_dynamic_memory
    def get_serializer(Class):
        from functools import partial
        from src.tools.serializers import Serializer
        # This object has two methods, parse and unparse
        return Serializer(Class, partial(Class.to_builtin), partial(Class.__from_builtin))

    ######################
    ##       FILE       ##
    ## SAVING & LOADING ##
    ######################
    
    def save(self, directory, filename = None, extension = "json"):
        if filename:
            filename = "{f}.{ext}".format(f=filename, ext=extension)
        else:
            filename = self.filename(extension)
        fullpath = os.join(directory, filename)
        serializer = self.get_serializer()
        result = serializer.parse(self)
        with open(fullpath, 'w') as f:
            f.write(result)
   
   
    @classmethod
    def load_from_filename(Class, directory, filename = None, extension = "json"):
        if filename:
            filename = "{f}.{ext}".format(f=filename, ext=extension)
        else:
            filename = self.filename(extension)
        fullpath = os.join(directory, filename)
        serializer = self.get_serializer()
        with open(fullpath, 'r') as f:
            content = f.read()
            
        return serializer.unparse(content)
   
   
    @classmethod
    def load_from_keys(Class, directory, extension = "json", **keywords):
        filename = self.filename(extension)
        fullpath = os.join(directory, filename)
        serializer = self.get_serializer()
        with open(fullpath, 'r') as f:
            content = f.read()
            
        return serializer.unparse(content, check_keys = get_keys(**keywords))
   
   
    @classmethod
    def load_from_server(Class, directory, filename = None, extension = "json"):
        # MUST IMPLEMENT VERY SOON
        ...
   
   
   
    
    # TO BE IMPLEMENTED IN SUBCLASSES
    
    def to_builtin(self):
        raise NotImplementedError("{s.__class__} does not implement the method 'to_builtin'. Create a subclass instead.".format(s=self))
        
    @classmethod
    def from_builtin(Class, builtin_obj, *, metadata = None):
        # metadata is optional
        raise NotImplementedError("{c} does not implement the classmethod 'from_builtin'. Create a subclass instead.".format(c=Class))
    
    @classmethod
    def check_consistency (Class, builtin_obj, metadata = None):
        # return boolean value
        raise NotImplementedError("{c} does not implement the classmethod 'check_consistency'. Create a subclass instead.".format(c=Class))
    

    
    
    
    
    #############################################################
    # PRIVATE
    @classmethod
    def __from_builtin(Class, builtin_obj, *, metadata = None, check_keys = {}):
            kwargs = {'check_keys' = check_keys}
        if metadata is not None:
            kwargs['metadata'] = metadata
        
        if Class.check_consistency(builtin_obj, **kwargs):
            return Class.from_builtin(builtin_obj, **kwargs)
        else:
            raise DataCorruptedError(builtin_obj, "Metadata: {metadata}", metadata=metadata)
    ############################################################