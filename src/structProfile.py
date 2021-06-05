from src.profile import Profile


class StructProfile(Profile):
    template_string = None
    template_dict = None
    dotbracket_string = None
    dotbracket_dict = None
    alphabet = None

    def __init__(self, profile, name, alpha):
        super().__init__(profile, name)
        self.alphabet = alpha

    def setTemplate(self,template):
        self.template_string = template

    def setDotbracket(self,db):
        self.dotbracket_string = db

    def setDictTemplate(self,d_template):
        self.template_dict = d_template

    def setDictDotbracket(self,d_db):
        self.dotbracket_dict = d_db

    def getTemplate(self):
        return self.template_string

    def getDotbracket(self):
        return self.dotbracket_string

    def getDictTemplate(self):
        return self.template_dict

    def getDictDotbracket(self):
        return self.dotbracket_dict

    def getAlphabet(self):
        return self.alphabet