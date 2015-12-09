from .abstract import OGSElement, OGSBetaElement
from ..players import Player


class OGSMacroPlayer(Player):
    # ABSTRACT OVERRIDES
    
    @classmethod
    def request_from_server (Class, credentials, request_type = 'id', **kwargs):
        if request_type == 'id':
            id = kwargs['id']
            return credentials.get(['players', id])
        else:
            return NotImplemented
    
    @classmethod
    def unpack(Class, package, request_type = 'id', **kwargs):
        if request_type == 'id':
            for key in ["rating","rating_blitz","rating_live","rating_correspondence"]:
                package[key]=float(package[key])
            # Transform date string...
            return package
        else:
            return NotImplemented
        
        

            


class OGSPlayer(OGSElement, OGSMacroPlayer):
    ...

class OGSBetaPlayer(OGSBetaElement, OGSMacroPlayer):
    ...
    
