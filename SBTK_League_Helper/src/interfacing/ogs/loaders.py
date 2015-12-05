# All content provided by the loader
# must come from canonical sources
# found in the implementation of this server interface
# (within src/interfacing/ogs/)

# This module should not create *any* original content
# other than the loader 

# Specifications of the keys the loader should provide
# can be found in src/interfacing/servers.py

# All imports go inside the functions
# otherwise, there is no point in doing it this way.

def main_loader() -> dict:
    result = {}

    from .resources import main_server_strings as strings
    result['str_name'] = strings['context']
    result['str_shortname'] = strings['context_short']
    
    result['bool_tester'] = False
    
    from .connect import Authentication
    result['cls_auth'] = Authentication
    result['list_authkeys'] = ['user', 'password'] # original content, beware
    
    from .players import OGSPlayer
    result['cls_player'] = OGSPlayer
    from .tournaments import OGSTournament
    result['cls_tournament'] = OGSTournament
    
    return result

    
def beta_loader() -> dict:
    result = {}

    from .resources import beta_server_strings as strings
    result['str_name'] = strings['context']
    result['str_shortname'] = strings['context_short']
    
    result['bool_tester'] = True
    
    from .connect import Authentication
    from functools import partial, wraps
    result['cls_auth'] = wraps(Authentication)(partial(Authentication, testing = True))
    result['list_authkeys'] = ['user', 'password'] # original content, beware
    
    from .players import OGSBetaPlayer
    result['cls_player'] = OGSBetaPlayer
    from .tournaments import OGSBetaTournament
    result['cls_tournament'] = OGSBetaTournament
    
    return result
    