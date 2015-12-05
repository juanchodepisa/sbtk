from collections import UserDict
from datetime import datetime
from urllib.parse import quote, unquote
from os import path

from src import application_encoding
from src.tools.date_time import utc, localtz
from src.tools.dynamic_programming import simple_dynamic_memory
from .exceptions import DataCorruptedError

class ServerElement(UserDict):
## This is a simple pseudo-abstract class
    def __init__(self, server, id, info, timestamp = None):
        if timestamp:
            self.__timestamp = timestamp
        else:
            # always normalize with UTC, otherwise nightmares ensue
            # represent the age of the info.
            self.__timestamp = datetime.now(tz = utc)
        self.__server = server
        self.__server_shortname = server.shortname
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
    def __metadata__(self):
        return dict(
            id = self.__id,
            server = self.__server_shortname,
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
        from src.tools.serializers import JSONSerializer
        # This object has two methods, parse and unparse
        return JSONSerializer(Class, partial(Class.to_builtin), partial(Class.__from_builtin))

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
        with open(fullpath, 'w', encoding = application_encoding) as f:
            f.write(result)
   
   
    @classmethod
    def load_from_filename(Class, directory, filename, extension = "json"):
        filename = "{f}.{ext}".format(f=filename, ext=extension)
        fullpath = os.join(directory, filename)
        serializer = Class.get_serializer()
        with open(fullpath, 'r', encoding = application_encoding) as f:
            content = f.read()
            
        return serializer.unparse(content)
   
   
    @classmethod
    def load_from_keys(Class, directory, extension = "json", **keywords):
        # keywords should coincide with the arguments from standard_filename
        filename = Class.standard_filename(extension = extension, **keywords)
        fullpath = os.join(directory, filename)
        serializer = Class.get_serializer()
        with open(fullpath, 'r', encoding = application_encoding) as f:
            content = f.read()
            
        return serializer.unparse(content, check_keys = Class.get_keys(**keywords))

    ##################
    ##  EXTRACTING  ##
    ## FROM THE WEB ##
    ##################
   
    @classmethod
    def load_from_server(Class, credentials, request_type = "id", **kwargs):
        keywords = Class.request_kwarguments(request_type, **kwargs)
        raw = credentials(**keywords)
        builtin = Class.unpack(raw, request_type = request_type, **kwargs)
        return Class.from_builtin(builtin)
   
   
    @classmethod
    def load_batch_from_server(Class, credentials, request_type, **kwargs):
        keywords = Class.batch_request_kwarguments(request_type, **kwargs)
        raw = credentials(**keywords)
        builtins, metadata = Class.unbatch(raw, request_type = request_type, **kwargs)
        return [Class.from_builtin(builtin) for builtin in builtins], metadata
   
   
   
    ################################################
    # TO BE IMPLEMENTED IN SUBCLASSES
    
    # Parsing...
    
    def to_builtin(self):
        raise NotImplementedError("{s.__class__} does not implement the method 'to_builtin'. Create a subclass instead or override the method.".format(s=self))
        
    @classmethod
    def from_builtin(Class, builtin_obj, *, metadata = None):
        # metadata is optional
        raise NotImplementedError("{c} does not implement the classmethod 'from_builtin'. Create a subclass instead or override the method.".format(c=Class))
    
    @classmethod
    def check_consistency (Class, builtin_obj, metadata = None) -> bool:
        raise NotImplementedError("{c} does not implement the classmethod 'check_consistency'. Create a subclass instead or override the method.".format(c=Class))
    
    
    # Web requests...
    
    @classmethod
    def request_kwarguments (Class, request_type = 'id', **kwargs) -> "keywords":
        raise NotImplementedError("{c} does not implement the classmethod 'request_kwarguments'. Create a subclass instead or override the method.".format(c=Class))
    
    @classmethod
        raise NotImplementedError("{c} does not implement the classmethod 'unpack'. Create a subclass instead or override the method.".format(c=Class))

    
    @classmethod
    def batch_request_kwarguments (Class, request_type, **kwargs) -> "keywords":
        raise NotImplementedError("{c} does not implement the classmethod 'batch_request_kwarguments'. Create a subclass instead or override the method.".format(c=Class))
    
    @classmethod
    def unbatch (Class, batch, request_type, **kwargs) -> ("iterable of builtins", "metadata"):
        raise NotImplementedError("{c} does not implement the classmethod 'unbatch'. Create a subclass instead or override the method.".format(c=Class))
    
    ################################################
    
    
    
    
    #############################################################
    # PRIVATE
    @classmethod
    def __from_builtin(Class, builtin_obj, *, metadata = None):
        kwargs = {}
        if metadata is not None:
            kwargs['metadata'] = metadata
        
        if Class.check_consistency(builtin_obj, **kwargs):
            return Class.from_builtin(builtin_obj, **kwargs)
        else:
            raise DataCorruptedError(builtin_obj, "Metadata: {metadata}", metadata=metadata)
    ############################################################