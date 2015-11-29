# This need to be sorted out in a smarter way

class InitializationError(Exception):
    def __init__(self, SomeClass, description):
        self.value = SomeClass
        self.description = description.format(SomeClass.__name__)
    
    def __str__(self):
        return self.description

class ReservedValueError(Exception):
    def __init__(self, expected, received, description):
        self.value= received
        self.expected = expected
        self.description = description.format(expected, received)
    
    def __str__(self):
        return self.description
        

class ApplicationError(Exception):
    pass
    
class NonFatalError(ApplicationError):
    pass

class FatalError(Exception):
    pass

class UserError(NonFatalError):
    pass