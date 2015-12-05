from .drawing import BoxDrawingOperations, BufferedMatrix_CP850


class ConsoleDisplayObject(object):
    def __init__(self, parent):
        self.parent = parent
        if parent is not None:
            parent.add_child(self)
        self.__callback = lambda slf , evnt: None
        self.__trigger_fun = lambda evnt: False
        self.__show = True

    def __call__(self, event):
        if self.__trigger_fun(event):
            self.__callback(self, event)
            return True
        else:
            return False
            
    def show (self):
        if not self.__show:
            self.__show = True
            if self.parent is not None:
                self.parent.show_child(self)

    def hide (self):
        if self.__show:
            self.__show = False
            if self.parent is not None:
                self.parent.hide_child(self)
    
    def flush(self):
        raise NotImplementedError("flush method is not yet implemented by {}".format(type(self)))
        
    def __str__(self):
        try:
            return self.string # This string must be created in the subclasses
        except AttributeError:
            raise NotImplementedError("string field is not yet created by {}".format(type(self)))
        
    
    def set_trigger (self, function): # function that evaluates an event
        self.__trigger_fun = function
    def set_callback (self, function):
        self.__callback = function
    
    
    

class Container(ConsoleDisplayObject):
    def __init__(self, parent):
        super(ConsoleDisplayObject, self).__init__(self, parent)
        self.children = []
    
    def add_child(self, child):
        self.children.append((child, {"show": True}))
    
    def show_child(self, child):
        raise NotImplementedError("show_child method is not yet implemented by {}".format(type(self)))
    
    def hide_child(self, child):
        raise NotImplementedError("hide_child method is not yet implemented by {}".format(type(self)))        
        
    
    

class NonContainer(ConsoleDisplayObject):
    pass


    
    
class Window(Container):
    pass
    