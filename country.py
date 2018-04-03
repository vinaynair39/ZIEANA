import json
import requests


class Countries:

    def capital(self, country):
        r = requests.get('https://restcountries.eu/rest/v2/name/{}'.format(country))
        data = json.loads(r.text)
        capital = data[0]['capital']
        return "The capital of {} is {}.".format(country, capital)



    def population(self, country):
        r = requests.get('https://restcountries.eu/rest/v2/name/{}'.format(country))
        data = json.loads(r.text)
        population = data[0]['population']
        return "{} has a population of about {}".format(country, population)


    def currency(self, country):
        r = requests.get('https://restcountries.eu/rest/v2/name/{}'.format(country))
        data = json.loads(r.text)
        currency = data[0]['currencies'][0]['name']
        return "The currency of {} is {}".format(country, currency)

    def country_info(self, country):
        dict1 = dict()
        r = requests.get('https://restcountries.eu/rest/v2/name/{}'.format(country))
        data = json.loads(r.text)
        population = data[0]['population']
        flag = data[0]['flag']
        capital = data[0]['capital']
        continent = data[0]['region']
        text = "{} is located in {}. The capital of {} is {} and they have a population of about {}.".format(country, continent, country, capital, population)
        dict1 = {'info': text, 'flag': flag}
        return dict1

if __name__ == '__main__':
    obj = Countries()
    data = obj.country_info(input())
    print(data)







