class ParameterTypeError (Exception):
    def __init__(self, parameters, expected, location):
        self.value = parameters
        self.expected = expected
        self.location = location
        self.description = "Keywords in file %s should match the following parameters: %r. Found keywords: %r." % (location, expected, parameters)
        
    def __str__(self):
        return repr(self.description)
        

class TypeUnsupportedError (Exception):    
    def __str__(self):
        return repr(self.description)

class FileTypeUnsupportedError (TypeUnsupportedError):
    def __init__(self, filename, operation, type=""): # operation: 'read', 'write', etc.
        self.value = filename
        if type:
            self.type = type
        else:
            type = self.type = filename.split(".")[-1]
        self.operation = operation
        self.description = "Cannot {0} {1}. ".format(filename, operation)
        if type:
            self.description += "File type {} is unsupported.".format(type)
        else:
            self.description += "File type is unknown."

class TypeParseError(TypeUnsupportedError):
    def __init__(self, content_type, method = 'POST'):
        self.value = content_type
        self.method = method
        self.description = "Content type %s is not yet supported for parsing into a %s HTTP request." % (content_type, method)

class TypeUnparseError(TypeUnsupportedError):
    def __init__(self, content_type):
        self.value = content_type
        self.description = "Content type %s is not yet supported for unparsing from web content." % content_type