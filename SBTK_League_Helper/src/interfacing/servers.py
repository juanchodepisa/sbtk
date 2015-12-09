from src.tools.dictionaries import PostLoadedDict

# Utility class
################################################
class ServerImplementationDict(PostLoadedDict):
    def __missing__(self, key):
        try:
            return super().__missing__(key)
        except KeyError:
            return NotImplemented
################################################



class Server():
    def __init__(self, shortname, loader):
        # Not preloaded
        # loaders must produce dictionaries (or an appropriate iterable)
        # with the required keys.
        # The reason for this is that code for certain servers need not be loaded
        # if it's not going to be used at all
        # It also prevents import loop collisions.
        global __ServerImplementationDict
        self.__data = ServerImplementationDict(loader)
        self.__shortname = shortname
    
    @property
    def shortname(self):
    # This is the only property provided from above
        return self.__shortname
        
    def __str__(self):
        return str(self.__shortname)
        
    # All other properties must come from canonical sources
    # provided by the server loader
    
    # CONSTANTS (STRINGS, BOOLEANS, INTS, ETC.)
    
    @property
    def name(self):
        return self.__data['str_name']
        
    @property
    def internal_shortname(self):
        return self.__data['str_shortname']
        
    @property
    def beta(self):
        return self.__data['bool_tester']
    
    
    # CLASSES
    
    # 1- Credentials:
    
    @property
    def Auth(self): # I really don't know how to call this.
        return self.__data['cls_auth']
    @property
    def auth_fields(self):
        return self.__data['list_authkeys']
        
    # 2- Server Elements:
    
    @property
    def Player(self):
        return self.__data['cls_player']
    
    @property
    def Tournament(self):
        return self.__data['cls_tournament']