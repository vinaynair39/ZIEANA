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

    def acknowledge(self):

        user_name = self.user_name
        if user_name is None:
            user_name = ""

        simple_acknoledgement = [
            "Yes?",
            "What can I do for you?",
            "How can I help?"
        ]

        date = datetime.datetime.now()
        time_acknowledgement = [
            f"Good {self.time_of_day(date)}. What can I do for you?",
            f"hey! Good {self.time_of_day(date)}. How can I help? ",
            f"Hello there! Good {self.time_of_day(date)}. How can I help you? ",
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
            choice = random.randint(1, 2)   # gives   1 or 2
        else:
            choice = random.randint(0, 1)    # gives 0

        ret_phrase = ""

        if choice == 0:
            ret_phrase = random.choice(simple_acknoledgement)
        elif choice == 1:
            ret_phrase = random.choice(time_acknowledgement)
        else:
            ret_phrase = random.choice(personal_acknowledgement)

        return ret_phrase


    def forecast(self, forecast_obj):

        ret_phrase = ""
        forecast = ""

        if forecast_obj.get("forecast") is None:
            return ret_phrase
        else:
            forecast = forecast_obj.get("forecast")

        forecast_current = [
            "Currently, it's",
            "Right now, it's",
            "At the moment, it's",
            "It's",
            "It is"
        ]

        forecast_hourly = [
            "It's",
            "It will be",
            "Looks like it will be"
        ]

        forecast_daily = [
            ""
        ]

        if forecast_obj.get('forecast_type') == "current":
            ret_phrase = "%s %s" % (random.choice(forecast_current), forecast)
        elif forecast_obj.get('forecast_type') == "hourly":
            ret_phrase = "%s %s" % (random.choice(forecast_hourly), forecast)
        elif forecast_obj.get('forecast_type') == "daily":
            ret_phrase = "%s %s" % (random.choice(forecast_daily), forecast)

        return ret_phrase

