def class_initializer(Class): # I don't know why there isn't a normal convention for this.
    convention = "__initClass__"
    #convention = "_%s%s" % (Class.__name__, convention) # mangled name, not necessary in this case
    method = getattr(Class, convention)
    method()
    return Class