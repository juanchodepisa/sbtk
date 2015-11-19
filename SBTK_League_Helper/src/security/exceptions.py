class PasswordError(Exception):
    def __init__(self, message = ""):
        self.description = "Invalid password."
        if message:
            self.description += " " + message
        
    def __str__(self):
        return repr(self.description)
        
class PasswordLengthError(PasswordError):
    def __init__(self, password_lenght, minimum_length):
        self.value = password_lenght
        self.minimum = minimum_length
        self.description = "Password has only %d characters (Valid passwords must have at least %d characters)." % (self.value, minimum_length)
        super(PasswordLengthError, self).__init__(self.description)
        
        
class PasswordCharacterError(PasswordError):
    def __init__(self, character):
        self.value=character
        self.description = "Password contains %r (Valid passwords characters: a-z, A-Z, 0-9, '-' and '.')." % self.value
        super(PasswordCharacterError, self).__init__(self.description)



class KeysAddressError(Exception):
    pass

    
class KeysDirectoryNotFound(KeysAddressError):
    def __init__(self, user):
        self.value=user
        self.description = "No valid directory was found or provided for user %s." % user
        
    def __str__(self):
        return repr(self.description)


class KeysFileNotFound(KeysAddressError):
    def __init__(self, user, filename):
        self.value=user
        self.filename=filename
        self.description = "File containing the keys could not be found for user %s. Expected file path: %s" % (user, filename)
        
    def __str__(self):
        return repr(self.description)