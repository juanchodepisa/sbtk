from src.mvp_requirements import Controller

class Manager(Controller):
    def __init__(self, UIClass, *args, **kwargs):
        self.__user_interface = UIClass(self)
        
    def main_loop(self):
        self.__user_interface.main_loop()
    


    