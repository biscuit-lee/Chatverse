

""" BOTS LOGIC
    BOTS TWEETS WHEN  someone @ to him
    BOTS tweets when someone he follows post thigns if he has any opinions on the post
    BOTS subscribe to the news
    should bots have memories?
""" 
class Bots:
    def __init__(self, name, prompt, tweet_interval):
        self.name = name
        self.prompt = prompt
        self.tweet_interval = tweet_interval
        

    def get_name(self):
        return self.name
    def get_prompt(self):
        return self.prompt

    def follow(username):
        pass