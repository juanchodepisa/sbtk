# These are abstract classes
# an enumeration of the methods that need to be implemented for their instances.

class UserInterface (object):
    def __init__(self, boss, *args, **kwargs): #args and kwargs may optionally have an effect
        raise NotImplementedError
    
    def main_loop(self):
        raise NotImplementedError() # must bring the main loop to front
        


class Controller (object):
    def __init__(self, UIClass, *args, **kwargs): #args and kwargs may optionally have an effect
        raise NotImplementedError()
    
    def main_loop(self):
        raise NotImplementedError() # must ask the ui for the loop