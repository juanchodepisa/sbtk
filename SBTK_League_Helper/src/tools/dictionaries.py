from .markers import AdHocMarker
from .exceptions import InitializationError, ReservedValueError


class MarkedDict(dict): # This class and its subclasses always require initialization before use.
    __initialized = None #Indicates the closest initialized superclass (of MarkedDict type) 
    
    # By (my own) convention:
    # the first element must be the "default" marker.
    # this is reenforced in __initClass__
    # the name is reserved, don't try to change it.
    __defined_markers = ("default",)            #These can be extended through subclasses
    __default_str="default"
    __default_marker = None
    
    __markers_index = {}
    
    # Independent reference markers, not logged to the list above:
    # they are left public for access, but don't mess with them
    __root_marker  = None # Root reference
    __path_marker  = None # Reference to its path
    __self_marker  = None # Reference to itself
    __up_marker    = None # Reference to its container
    __id_marker    = None # Generic id reference
    __short_marker = None # Reference to shortcuts
    __parse_marker = None # Reference to an id parser function

    __ref_markers_index = {}

    __all_markers = ()
    
    __display_fields__ = ("default",)
    __display_indentation__ = 4
    
    
    
    def __init__(*args, **kwargs): 
        
        self = args[0] # dirty trick, to avoid reserving the name in the outside scope, no need to check, as it's only passed through "."
        args = args[1:]
        
        if self.__not_initialized():
            raise InitializationError(type(self),
                "\n Class {} has not been initialized.\n It requires initialization before creating any instances thereof.\n Use the class_initializer method in the package.")
        
        rt = self.__root_marker
        pa = self.__path_marker
        sf = self.__self_marker
        up = self.__up_marker
        
        dict1 = {rt: self, sf: self, up:None, pa: [rt]}
        dict2 = dict(*args,**kwargs)
        dict1.update(dict2) # so that keys can be overriden
        super(MarkedDict, self).__init__(dict1)
    
    
    @classmethod
    def __not_initialized(Class):
        return not Class.__initialized is Class
        

    @classmethod
    def marker(Class, key):
        return Class.__markers_index[key]
        
    @classmethod
    def ref_marker(Class, key):
        return Class.__ref_markers_index[key]
        
    @classmethod
    def is_ref_marker(Class, marker, id = True, shortcut = True):
        if marker is Class.__id_marker:
            return bool(id)
        elif marker is Class.__short_marker:
            return bool(shortcut)
        else:
            for key, value in Class.__ref_markers_index.items():
                if marker is value:
                    return True
                    break
            else:
                return False
        
    @classmethod
    def is_marker(Class, marker, default = True):
        if marker is Class.__default_marker:
            return bool(default)
        else:
            for key, value in Class.__markers_index.items():
                if marker is value:
                    return True
                    break
            else:
                return False
        
    @classmethod
    def is_any_marker(Class, marker, id = True, shortcut = True):
        if marker is Class.__id_marker:
            return bool(id)
        elif marker is Class.__short_marker:
            return bool(shortcut)
        else:
            return marker in Class.__all_markers
        
    @classmethod
    def set_markers(Class, *custom_markers):
        if Class.__not_initialized():
            if custom_markers[0]=="default":
                Class.__defined_markers = tuple(custom_markers)
            else:
                raise ReservedValueError("default", custom_markers[0],"The first marker must always be {}. Got {}")
        else:
            raise InitializationError(Class, "\n Class {} has already been initialized.\n Should set markers again, create a subclass instead.")
            
    
    def is_legitimate_node(self, key, ID = True, SHORTCUT = True):
        if key in self.__all_markers:
            if key is self.__id_marker and key in self:
                return bool(ID)
            elif key is self.__short_marker and key in self:
                return bool(SHORTCUT)
            else:
                return False
        else:
            return key in self
    
    def display_condition(*any):
        return True
    
    
    
    def add (*args, **kwargs): 
    # def add (self, path, **kwargs): checking then assigning
    # Add function is shortcut safe, so original paths should be used. See add_shortcut below.
        __len = len(args)
        __exp = 2
        if __len!=__exp:
            error_str = "%s() takes %d positional arguments but %d were given" % (type(self).add.__name__, __exp, __len)
            raise TypeError(error_str)

        self = args[0]# dirty trick, to avoid reserving the names in the outside scope
        path = args[1]
        
        rt = self.__root_marker
        pa = self.__path_marker
        sf = self.__self_marker
        up = self.__up_marker
    
        dictR = self[rt] # ROOT
        dict0 = self[up] # UP
        dict1 = self     # SELF
        path1 = self[pa] # PATH
        
        for id in path:
            dict0 = dict1
            path1 = path1 + [id]
            try:
                dict1 = dict1[id]
            except KeyError:
                dict1[id]=type(self)({rt: dictR, up: dict0, pa:path1})
                dict1 = dict1[id]
        
        dict2 = {self.marker(key): value for key, value in kwargs.items()} # AUX
        dict1.update(dict2)
        return dict1
    
    def __call__ (self, path=[], inquiry = "default", shortcut_safe = False , SELF = False, UP = False, formatting_function=str.format, unformatted = False):
        id = self.__id_marker
        sh = self.__short_marker
        ps = self.__parse_marker
    
        id_list = [] # IDs
        dict1 = self # SELF
        prev_key = None
        parse_dict = None
        
        for key in path:
            
            if key is id: id_list = list(id_list) + [id] # This is for explicit ID. Thread with care with formatting
            if prev_key is sh: # This is for explicit shortcut
                id_list = parse_dict[key](*id_list)
            
            try: # Normal way
                dict1 = dict1[key]
            except KeyError:
                try: # Through shortcut
                    if shortcut_safe: raise KeyError("Shortcut safe inquiry. Key not found: %s" % key)
                    dict_sh = dict1[sh]
                    dict1 = dict_sh[key]
                except KeyError:
                    try: # Through ID
                        dict1 = dict1[id]
                        id_list = list(id_list) + [key]
                    except KeyError: # Through ID within a shortcut
                        if shortcut_safe: raise KeyError("Shortcut safe inquiry. Key not found: %s" % key)
                        dict_sh = dict1[sh]
                        dict1 = dict_sh[id]
                        id_list = list(id_list) + [key]
                        parse_fun = dict_sh[ps][id]
                        id_list = parse_fun(*id_list)
                else: # This means we got through the shortcut, the normal way
                    parse_fun = dict_sh[ps][key]
                    id_list = parse_fun(*id_list)
            
            if key is sh: parse_dict = dict1[ps] # This is for explicit shortcut
            prev_key = key
                
        ## NOTE: There must always be a parsing function for every shortcut, even if it is the identity.
        ##      Notice that parsing functions are flattened, so they might take positional arguments.
        

        if SELF:
            return (dict1[self.__self_marker], id_list)
        elif UP:
            return (dict1[self.__up_marker], id_list)
        elif unformatted:
            return [dict1[self.marker(inquiry)], id_list]
        else:
            return formatting_function( dict1[self.marker(inquiry)], *id_list)
            
    
    def add_shortcut (self, path1, path2, parsing_function = lambda *args : list(args)):
        sh = self.__short_marker
        ps = self.__parse_marker
        
        destination = self(path2, SELF = True)[0] #must exist
        
        path1 = list(path1) # Normalization
        shct_id = path1[-1] # The name we want to bind
        path1[-1] = sh
        dict_sh = self.add(path1) # Contents of the special shortcut node
        
        dict_sh[shct_id] = destination
        
        try:
            parse_dict = dict_sh[ps]
            parse_dict.update({shct_id: parsing_function})
        except KeyError:
            dict_sh[ps] = {shct_id: parsing_function}
        
    
    def __str__(self):
        result = "<class {}> instance:\n\n".format(type(self).__name__)
        header = str(self[self.__path_marker])
        
        def node2str(self, header, trailing, last_node = False, is_shortcut = False, firt_node=False):
            border_str = "\u2550" * (len(str(header))+2)
            indent_space = " " * self.__display_indentation__
            indent_line = "\u2500" * self.__display_indentation__
            
            omit_first_char = 2+self.__display_indentation__ if firt_node else 0
            
            result = "{}\u2502 {}\u2554{}\u2557\n".format(trailing, indent_space, border_str)[omit_first_char:]
            if last_node:
                result += "{}\u2514\u2500{}\u2551 {} \u2551\n".format(trailing, indent_line ,header)[omit_first_char:]
            else:
                result += "{}\u251c\u2500{}\u2551 {} \u2551\n".format(trailing, indent_line ,header)[omit_first_char:]
                
            trailing = trailing + ("  " if last_node else "\u2502 ") + indent_space
            if firt_node:
                trailing = trailing[omit_first_char:]
                
            result += "{}\u255a{}\u255d\n".format(trailing ,border_str)
            
            gen = list((x for x in self if not self.is_any_marker(x, id = False, shortcut = False) and self.display_condition(x)))
            
            if is_shortcut:
                for key in gen[:-1]:
                    result += "{}\u251c\u2500 {}:{}\n".format(trailing, key, self[key][self.__path_marker])
                key = gen[-1]
                result += "{}\u2514\u2500 {}:{}\n".format(trailing, key, self[key][self.__path_marker])
            else:
                for key in self.__display_fields__:
                    field = "{}: {}".format(key, self[self.marker(key)]).rstrip()
                    result += "{}\u2502\u251c {}\n".format(trailing ,field)
                if gen:
                    result += "{}\u251c\u2518\n".format(trailing ,header)
                    for key in gen[:-1]:
                        result += node2str(self[key], key, trailing, is_shortcut = key is self.__short_marker)
                    key = gen[-1]
                    result += node2str(self[key], key, trailing, last_node = True, is_shortcut = key is self.__short_marker)
                else:
                    result += "{}\u2514\u2518\n".format(trailing ,header)
            return result
        
        result += node2str(self, header, "", True, False, True)    
        
        return result
        
    
    
    @classmethod
    def __initClass__(Class): #This is my own convention. The class initializer will look for this method#
        if not Class.__not_initialized():
            raise InitializationError(Class, "\n Class {} has already been initialized.\n Should not initialize twice, create a subclass instead.")
        else:
            Class.__initialized = Class
        
        special_marker = AdHocMarker("#", Class) 
        Class.__markers_index = {key : AdHocMarker(key, Class) for key in Class.__defined_markers}
        Class.__default_str = "default"
        Class.__default_marker = Class.__markers_index[Class.__default_str]
        
        # Initializing reference markers
        Class.__root_marker = AdHocMarker("#ROOT#", special_marker)
        Class.__path_marker = AdHocMarker("#PATH#", special_marker)
        Class.__self_marker = AdHocMarker("#SELF#", special_marker)
        Class.__up_marker = AdHocMarker("#UP#", special_marker)
        Class.__id_marker = AdHocMarker("#ID#", special_marker)
        Class.__short_marker = AdHocMarker("#SHORTCUT#", special_marker)
        Class.__parse_marker = AdHocMarker("#IDPARSER#", special_marker)
        
        Class.__ref_markers_index = {
            "root":Class.__root_marker,
            "path":Class.__path_marker,
            "self":Class.__self_marker,
            "up":Class.__up_marker,
            "id":Class.__id_marker,
            "shortcut":Class.__short_marker,
            "id parser":Class.__parse_marker}
        
        Class.__all_markers = tuple(Class.__ref_markers_index.values()) + tuple(Class.__markers_index.values())
            