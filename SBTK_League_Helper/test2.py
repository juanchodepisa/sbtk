class Foo():
    def __init__(self,a,b):
        print ("init Foo", a, b)
        self.__a=a
        self.__b=b
    @property
    def a(self):
        return self.__a
    @property
    def b(self):
        return self.__b
    
    def name(self):
        print ("Foo")
        
    def aux(self):
        print("Hello")

    
class Bar(Foo):
    def __init__(self,a,b):
        print("init Bar", a, b)
        super().__init__(a,b)
    
    def name(self):
        print ("Bar")
        
    def aux(self):
        print("Howdy")

        
class Baz(Foo):
    def __init__(self,b):
        print("init Coco" , b)
        super().__init__(1,b)

    def name(self):
        print ("Baz")

class Qux(Baz, Bar):
    pass

d = Qux(9)