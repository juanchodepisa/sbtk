import sys

from manager.main_class import Manager
from user_interfaces.console_ui.ui import UserInterface


def digest_system_arguments():
    sys.argv # something, to be implemented later on.
    
    return ([],{}) #args and kwargs to be passed onto the manager.

    
def module_behavior():
    pass
    
    

def main():
    args, kwargs = digest_system_arguments()
    main_object = Manager(UserInterface, *args, **kwargs)
    main_object.main_loop()

    
if __name__ == "__main__":
    main()
else:
    module_behavior()