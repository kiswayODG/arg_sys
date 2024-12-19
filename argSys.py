
class ArgSys:
    arguments = []
    attaques = []
    

    @classmethod
    def set_arguments(cls,new_arguments):
        cls.arguments = new_arguments

    @classmethod
    def set_attaques(cls,new_attaques):
        cls.attaques = new_attaques

    @classmethod
    def get_arguments(cls):
        return cls.arguments

    @classmethod
    def get_attaques(cls):
        return cls.attaques