from abc import ABCMeta, abstractmethod

class Foo(metaclass=ABCMeta):
    @property
    @abstractmethod
    def hello(self):
        ...

class Bar(Foo):
    pass

class Baz(Foo):
    hello = "Hello Baz!!!"
