from src.tools.dictionaries import PostLoadedDict


class Server():
    def __init__(self, loader):
        # Not preloaded
        # loaders must produce dictionaries (or an appropriate iterable)
        # with the required keys.
        # The reason for this is that code for certain servers need not be loaded
        # if it's not going to be used at all
        self.__data = PostLoadedDict(loader)
        
    @property
    def name(self):
        return self.__data['name']
        
    @property
    def shortname(self):
        return self.__data['shortname']
        
    @property
    def beta(self):
        return self.__data['tester']

## THIS IS DEPRECATED, IT MUST BE IMPLEMENTED IN A MORE SPECIFIC WAY:
# supported_servers = {
    # "OGS": AdHocMarker("OGS", "Go Server"),
    # "OGS_Beta": AdHocMarker("OGS_Beta", "Beta Go Server")}