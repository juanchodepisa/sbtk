from ..abstract import ServerElement

from .resources import main_server, beta_server


class OGSElement(ServerElement):
    def __init__(self, id, info, timestamp = None):
        super().__init__(main_server, id, info, timestamp)

class OGSBetaElement(ServerElement):
    def __init__(self, id, info, timestamp = None):
        super().__init__(beta_server, id, info, timestamp)
        
    # This class possibly requires more detail, to add testing = True
    # as a keyword to inquiries.