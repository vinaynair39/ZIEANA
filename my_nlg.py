from random import random
import random
import datetime
class NLG(object):
    """
    Used to generate natural language. Most of these sections are hard coded. However, some use simpleNLG which is
    used to string together verbs and nouns.
    """
    def __init__(self, user_name=None):
        self.user_name = user_name

        # make random more random by seeding with time
        random.seed(datetime.datetime.now())

    def acknowledge(self):

        user_name = self.user_name
        if user_name is None:
            user_name = ""

        simple_acknoledgement = [
            "Yes?",
            "What can I do for you?",
            "How can I help?"
        ]

        personal_acknowledgement = [
            "How can I help you today, %s" % user_name,
            "How can I help you, %s" % user_name,
            "What can I do for you, %s" % user_name,
            "Hi %s, what can I do for you?" % user_name,
            "Hey %s, what can I do for you?" % user_name
        ]

        choice = 0
        if self.user_name is not None:
            choice = random.randint(0, 2)   # gives  0, 1 or 2
        else:
            choice = random.randint(0,1)    # gives 0 or 1

        ret_phrase = ""

        if choice == 0:
            ret_phrase = random.choice(simple_acknoledgement)
        elif choice == 1:
            date = datetime.datetime.now()
            ret_phrase = "Good %s. What can I do for you?" % self.time_of_day(date)
        else:
            ret_phrase = random.choice(personal_acknowledgement)

        return ret_phrase

    def time_of_day(self, date, with_adjective=False):
        ret_phrase = ""
        if date.hour < 10:
            ret_phrase = "morning"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)
        elif (date.hour >= 10) and (date.hour < 18):
            ret_phrase = "afternoon"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)
        elif date.hour >= 18:
            ret_phrase = "evening"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)

        return ret_phrase
