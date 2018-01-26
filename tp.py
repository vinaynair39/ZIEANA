from datetime import datetime
import time


class Holidays:

    def __init__(self):

        self.january = {
            '26 january': 'Republic day',
            '27 january': "nigga day"
        }

        self.february = {
            '14 february': 'Maha shivaratri',
            '19 february': 'Shivaji jayanti'
        }

        self.march = {
            '2 march': 'holi',
            '25 march': 'ram navami'
        }

    def find_next(self, month=None):
        data = list()
        if month is None:
            month = time.strftime('%B')
        if month.lower() == 'january':
            holiday = self.january
        elif month.lower() == 'february':
            holiday = self.february
        elif month.lower() == 'march':
            holiday = self.march
        for i, j in holiday.items():
            num = 0
            full_date = 2  # time.strftime('%d').lstrip('0')
            date = i.split(" ")
            if int(date[num]) > int(full_date):
                data += [i, j]
            num += 1
        return data

        # day = holiday.keys()
        # name = holiday.values()
        # data = list()
        # for i, j in zip(day, name):
        #     data += [i, j]
        # print(data)

if __name__ == '__main__':
    d = Holidays()
    data = d.find_next()
    count = len(data)
    print(count)


