from src import log_entry

from .servers import Server

# List of supported servers
# for external use the dict variable 'SUPPORTED_SERVERS' is provided instead

# to add a new server, simply add a short name for it into the __supported list
# and then update the get_loader()
# (also, don't forget to actually implement the server features ;) )

__supported = ['OGS', 'OGS_Beta'] #short strings

def __get_loader(name):
    loader = None
    if name == 'OGS':
        from .ogs.loaders import main_loader
        loader = main_loader
    elif name == 'OGS_Beta':
        from .ogs.loaders import beta_loader
        loader = beta_loader
    return __log_wrapper(name, loader)
        
        
def __log_wrapper(name, loader):
    def wrapper():
        ref = log_entry("Loading {} client tools...".format(name))
        result = loader()
        log_entry(ref, "Loaded!!!")
        return result
    return wrapper
        
#############


SUPPORTED_SERVERS = {}

for name in __supported:
    SUPPORTED_SERVERS[name] = Server(name, __get_loader(name))
    
del __supported, __get_loader, __log_wrapper, log_entry, Server