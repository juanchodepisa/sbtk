from ..abstract import ServerElement

from .resources import main_server, beta_server


class OGSElement(ServerElement):
    server = main_server
    server_shortname = str(server)
    
class OGSBetaElement(ServerElement):
    server = beta_server
    server_shortname = str(server)