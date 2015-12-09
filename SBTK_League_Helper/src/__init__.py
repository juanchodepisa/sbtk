from .script_msg_log import log_entry, waiting # Altering the print command to function as a log.


# APPLICATION-WIDE CONSTANTS
application_encoding = 'utf-8'
application_timeformat = "%Y-%m-%dT%H:%M:%S.%f%z" #ISO 8601 compliant (also readable back and forth)
application_user_agent = "STBK League Assistant/Pre-alpha https://github.com/juanchodepisa/sbtk"
# Exception base class for all
# custom created exceptions
application_BaseException = type('SBTKException',(Exception,),{})



def class_initializer(Class): # I don't know why there isn't a normal convention for this.
    convention = "__initClass__"
    #convention = "_%s%s" % (Class.__name__, convention) # mangled name, not necessary in this case
    method = getattr(Class, convention)
    method()
    return Class
    



