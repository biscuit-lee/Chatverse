

""" BOTS LOGIC
    BOTS TWEETS WHEN  someone @ to him
    BOTS tweets when someone he follows 

""" 
class Bots:
    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt

    def get_name(self):
        return self.name
    def get_prompt(self):
        return self.prompt
    