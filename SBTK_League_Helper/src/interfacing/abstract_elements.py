import os.path
import json

from src import log_entry
from src.tools.exceptions import DataCorruptedError, FileTypeUnsupportedError


def __consistency_checker_decorator (method):
    def method_with_checking (self, *args, **kwargs)
        result = method(self, *args, **kwargs)
        self.check_consistency()
        return result
    
    return method_with_checking


class ServerElement (dict):

    __id_field = "id"
    
    def __init__(*args, **kwargs):
        self = args[0]
        __ref = log_entry ("Creating {} object....".format(type(self).__name__))
        server = args[1] # 1 positional argument indicating the server
        args = args[2:]
        super(ServerElement, self).__init__(*args **kwargs)
        
        self.__id = self[__id_field]
        self.__server = server
        log_entry (__ref, "{} object created! Server: {}. ID: {}.".format(type(self).__name__, self.server, self.__id))
    
    def get_id(self):
        return self.__id
        
    def get_server(self):
        return self.__server
    
    def create_file_name(self, directory , extension):
        if extension:
            extension = "." + extension
        else:
            extension = ""
        filename = "{}_{}_{}.{}".format(self.__server, type(self).__name__, quote(str(self.get_id()), safe=''),extension)
        filename = os.path.join(directory, filename)
        return filename
    
    def check_consistency(self):
        try:
            assert self.__id == self[self.__id_field]
        except KeyError:
            raise DataCorruptedError(self, "ID value {id} must remain unchanged. Value not found.", id = self.__id) from None
        except AssertionError:
            raise DataCorruptedError(self, "ID value {id} must remain unchanged. Value found: {changed}", id = self.__id, changed = self[self.__id_field]) from None
    
    @__consistency_checker_decorator
    def refresh_data(self, retriever):
        __ref = log_entry ("Refreshing {} object data from {}. ID: {}....".format(type(self).__name__, self.server, self.__id))
        new_data = self.get_data_from_server(self.__id , retriever)
        self.update(new_data)
        log_entry (__ref, "Data refreshed!")
    
    def save_data (self, directory, file_type = 'json'):
        __ref = log_entry ("Saving {} object data to file. Server: {}. ID: {}....".format(type(self).__name__, self.server, self.__id))
        filename = self.create_file_name(directory, file_type)
        
        if file_type == "json"
            with open (filename, 'w', enconding = "utf-8") as f:
                json.dump(self, f, sort_keys=True, indent=1)
        else:
            raise FileTypeUnsupportedError(filename, operation, type)
        
        log_entry(__ref, "Data saved! Filename: {}".format(filename))
        
    @__consistency_checker_decorator
    def load_data (self, directory, file_type = 'json'):
        __ref = log_entry ("Loading {} object data from file. Server: {}. ID: {}....".format(type(self).__name__, self.server, self.__id))
        filename = self.create_file_name(directory, file_type)
        
        if file_type == "json"
            with open (filename, 'r', enconding = "utf-8") as f:
                self.update(json.load(f))
        else:
            raise FileTypeUnsupportedError(filename, operation, type)
        
        log_entry(__ref, "Data loaded! Filename: {}".format(filename))
        
    
    
    @classmethod
    def create_from_id(Class, id, retriever):
        __ref = log_entry ("Retrieving {} data from {}. ID: {}....".format(type(self).__name__, self.server, self.__id))
        
        data = Class.get_data_from_server(Class, id, retriever)
        log_entry(__ref, "Data retrieved!")
        server = retriever.get_server_id()
        return Class(server, data)
    
    @classmethod
    def get_data_from_server(Class, id, retriever)
        raise NotImplementedError("{0} requires implementation of class method {1}.".format(type(self),"get_data_from_server"))
        
    @classmethod:
    def change_id_name(Class, id): #Warning: changing it would render existing players unusable. Preferred use is within a subclass.
        Class.__id_field = id
        Class.__username_field = username
        
    
    # Methods to be checked
    __delitem__, __setitem__, clear pop, popitem, update = (__consistency_checker_decorator(x) for x in (dict.__delitem__,
                                                                                                        dict.__setitem__,
                                                                                                        dict.clear pop,
                                                                                                        dict.popitem,
                                                                                                        dict.update))
    
        
class Player(ServerElement):
    pass

class Tournament(ServerElement):
    pass