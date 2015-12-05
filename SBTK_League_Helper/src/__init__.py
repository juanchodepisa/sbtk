from .script_msg_log import log_entry, waiting # Altering the print command to function as a log.


application_encoding = 'utf-8'
application_user_agent = "STBK League Assistant/Pre-alpha https://github.com/juanchodepisa/sbtk"

def class_initializer(Class): # I don't know why there isn't a normal convention for this.
    convention = "__initClass__"
    #convention = "_%s%s" % (Class.__name__, convention) # mangled name, not necessary in this case
    method = getattr(Class, convention)
    method()
    return Class