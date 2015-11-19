class Partition (dict):
    def __init__(self):
        self.unique_partitions = []
        self.__is_flattened = False
        super(Partition, self).__init__() # a dictionary {element:container}
        
    def link (self, a, b):
        try:
            x = super(Partition, self).__getitem__(a)
            try:
                y = self[b]
                self[a] = self[b] = x.merge(y)
            except KeyError:
                x = x()
                x.append(b)
                self[a] = self[b] = x
        except KeyError:
            try:
                y = self[b]
                y.append(a)
                self[a] = self[b] = y
            except KeyError:
                self[a] = self[b] = DisjointSubset([a,b])
    
    def insert (self, a):
        try:
            self[a]
        except KeyError:
            self[a] = DisjointSubset([a])
    
    def __getitem__(self, a):
        x = super(Partition, self).__getitem__(a)()
        self[a] = x
        return x
    
    def flatten(self):
        for a in self:
            x = self[a]:
            if x.flatten():
                self.unique_partitions.append(x)
        self.__getitem__ = super(Partition, self).__getitem__
        self.__is_flattened = True        
        

class DisjointSubset(list):
    def __init__(self, elem):
        self.parent = None
        self.__is_flattened = False
        super(DisjointSubset, self).__init__([elem])
        
    def __call__(self):
        if self.parent:
            self.parent = self.parent()
            return self.parent
        else:
            return self
        
    def merge (self, other):
        if self.parent:
            self.parent = self.parent.merge(other)
            return self.parent
        else:
            self.parent=other()
            self.parent.extend(self)
            return self.parent
    
    def flatten (self):
        if self.__is_flattened:
            return False
        else:
            self.__is_flattened = True
            return True