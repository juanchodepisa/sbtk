from .servers import Server

# List of supported servers
# for external use the dict variable 'SUPPORTED_SERVERS' is provided instead

# to add a new server, simply add a short name for it into the __supported list
# and then update the get_loader()
# (also, don't forget to actually implement the server features ;) )

__supported = ['OGS', 'OGS_Beta']

def get_loader(name):
    if name == 'OGS':
        import .ogs.loaders
        return loaders.main_loader
    elif name == 'OGS_Beta':
        import .ogs.loaders
        return loaders.beta_loader
        
#############


SUPPORTED_SERVERS = {}

for name in __supported:
    SUPPORTED_SERVERS[name] = Server(name, get_loader(name))