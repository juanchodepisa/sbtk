from src.tools.markers import AdHocMarker

class Foo:
    def __new__(Class):
        print ("Foo new")
        super().__new__(Class)

    def __init__(self):
        print ("Foo init")
        super().__init__()

class Bar:
    def __new__(Class):
        print ("Bar new")
        super().__new__(Class)

    def __init__(self):
        print ("Bar init")
        super().__init__()
        
class someshit(Foo, Bar):
    pass
    
