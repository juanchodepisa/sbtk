# import user_interfaces.console_ui.mock_widgets.display_elements

# def deco (f):
    # def inner():
        # with context() as c:
            # f()
    # return inner

# class context():
    # def __enter__(self):
        # print ("entering")
        # return self
    
    # def foo (self):
        # print("bar")
    
    # def __exit__(self, exc_type, exc_value, traceback):
        # print ("exito")
        

# @deco
# def f():
    # c.foo()
    
import logging
logging.warning('{} before you {}', 'Look', 'leap!')