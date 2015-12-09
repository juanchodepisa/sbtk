from abc import ABCMeta, abstractmethod
from collections import UserDict
from datetime import datetime, timezone
from functools import partial, lru_cache
from os import path
from urllib.parse import quote, unquote

from src import application_encoding, application_timeformat

from . import SUPPORTED_SERVERS
from .exceptions import DataCorruptedError, WrongServerCredentials

class ServerElement(UserDict, metaclass = ABCMeta):
## This is a simple pseudo-abstract class
    def __init__(self, id, info, timestamp = None):
        if timestamp:
            self.__timestamp = timestamp
        else:
            # always normalize with UTC, otherwise nightmares ensue
            # represent the age of the info.
            self.__timestamp = datetime.now(tz = timezone.utc)
        self.__id = id
        super().__init__(info)
    
    ################
    ## PROPERTIES ##
    ## & METHODS  ##
    ################
    
    # Some of these exist to provide easy overrides

    server = None
    server_shortname = str(server)
    
    
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
            server = self.server,
            timestamp = self.__timestamp)
        
    @property
    def __formatted_metadata__(self):
        return dict(
            id = self.__id,
            server = self.server_shortname,
            timestamp = self.__timestamp.strftime(application_timeformat))
    
    @staticmethod
    def recover_metadata(formatted_dict):
        dic = formatted_dict.copy()
        dic['server'] = SUPPORTED_SERVERS[dic['server']]
        dic['timestamp'] = datetime.strptime(dic['server'], application_timeformat)
        return dic

    def filename(self, extension = "json"):
        return self.standard_filename(self.__id, extension = extension)
    
    @classmethod
    def standard_filename(Class, id , extension = "json"):
        return "{server}-{cls.__name__}-{cls.__module__}-{safeid}.{ext}".format(
            server=Class.server_shortname,
            cls=Class,
            safeid = quote(str(id), safe=""), 
            ext=extension)
    
    @classmethod
    def get_keys(Class, **kwargs):
        result = {'server' : Class.server_shortname}
        if 'id' in kwargs
            result['id'] = kwargs['id']
        return result
            
    ################
    ## SERIALIZER ##
    ##   OBJECT   ##
    ################
     
    @classmethod
    @lru_cache(maxsize=None)
    def get_serializer(Class):
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
        # without overrides, keywords = {'id' : ...}
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
        if credentials.server is not Class.server:
            raise WrongServerCredentials(credentials.server, Class)
        raw = Class.request_from_server(credentials, request_type, **kwargs)
        builtin = Class.unpack(raw, request_type = request_type, **kwargs)
        return Class.from_builtin(builtin)
   
   
    @classmethod
    def load_batch_from_server(Class, credentials, request_type, **kwargs):
        if credentials.server is not Class.server:
            raise WrongServerCredentials(credentials.server, Class)
        raw = Class.batch_request_from_server(credentials, request_type, **kwargs)
        builtins, processed_metadata = Class.unbatch(raw, request_type = request_type, **kwargs)
        return [Class.from_builtin(builtin) for builtin in builtins], processed_metadata
   
   
   
    ################################################
    # ABSTRACT METHODS
    #
    # TO BE IMPLEMENTED IN SUBCLASSES
    # Override these methods to keep the implemention
    # as uniform as possible.
    
    # Parsing...
    
    @abstractmethod
    def to_builtin(self) -> dict:
        ...
        
    @classmethod
    @abstractmethod
    def from_builtin(Class, builtin_obj, *, metadata = None) -> "object of its class":
        # metadata is optional
        ...
    
    @classmethod
    @abstractmethod
    def check_consistency (Class, builtin_obj, metadata = None) -> bool:
        ...
    
    
    # Web requests (Server specific)...
    
    @classmethod
    @abstractmethod
    def request_from_server (Class, credentials, request_type = 'id', **kwargs) -> "server response":
        ...
    
    @classmethod
    @abstractmethod
    def unpack (Class, package, request_type, **kwargs) -> "builtin":
        # WARNING!
        # Can be destructive on the package.
        # For preservation, use a copy.
        ...

    
    @classmethod
    @abstractmethod
    def batch_request_from_server (Class, credentials, request_type, **kwargs) -> "server response":
        ...
    
    @classmethod
    @abstractmethod
    def unbatch (Class, batch, request_type, **kwargs) -> ("iterable of builtins", "metadata"):
        # WARNING!
        # Can be destructive on the batch.
        # For preservation, use a copy.
        ...
    
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