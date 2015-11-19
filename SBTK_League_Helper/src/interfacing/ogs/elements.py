from .. import abstract_elements

class OGSProperElement(abstract_elements.ServerElement):
    resource_tree_path = [] #This field must be overriden for every subclass
    
    @classmethod
    def get_data_from_server(Class, id, retriever): # The retriever is an auth object
        retriever.get (resource_tree_path+[id])


        

class Player (OGSProperElement, abstract_elements.Player):
    resource_tree_path = ['players']

class Tournament (OGSProperElement, abstract_elements.Tournament):
    resource_tree_path = ['tournaments']

