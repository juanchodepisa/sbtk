from src import application_timeformat
from datetime import datetime

from .abstract import ServerElement

class Player (ServerElement):

    # ABSTRACT OVERRIDES:
    
    def to_builtin(self):
        d = self.data.copy()
        try:
            d['registration_date'] = d['registration_date'].strftime(application_timeformat)
        return d
    
    @classmethod
    def from_builtin(Class, builtin_obj, *, metadata = None):
        if not metadata:
            metadata = {}
        
        try:
            id = metadata['id']
        except KeyError:
            id = builtin_obj['id']
        try:
            timestamp = metadata['timestamp']
        except KeyError:
            timestamp = None
        info = dict(builtin_obj)
        
        try:
            info['registration_date'] = datetime.strptime(info['registration_date'], application_timeformat)
        
        return Class(id=id, info=info, timestamp=timestamp)
    
    @classmethod
    def check_consistency(Class, builtin_obj, metadata = None):
        result =
            'id' in builtin_obj and
            ('id' not in metadata or builtin_obj['id'] == metadata['id']) and
            ('server' not in metadata or metadata['server'] == Class.server_shortname)
        return result