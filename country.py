import json
import requests


class Countries:

    def capital(self, country):
        r = requests.get(f'https://restcountries.eu/rest/v2/name/{country}')
        data = json.loads(r.text)
        capital = data[0]['capital']
        return f"The capital of {country} is {capital}."



    def population(self, country):
        r = requests.get(f'https://restcountries.eu/rest/v2/name/{country}')
        data = json.loads(r.text)
        population = data[0]['population']
        return f"{country} has a population of about {population}"


    def currency(self, country):
        r = requests.get(f'https://restcountries.eu/rest/v2/name/{country}')
        data = json.loads(r.text)
        currency = data[0]['currencies'][0]['name']
        return f"The currency of {country} is {currency}"

    def country_info(self, country):
        dict1 = dict()
        r = requests.get(f'https://restcountries.eu/rest/v2/name/{country}')
        data = json.loads(r.text)
        population = data[0]['population']
        flag = data[0]['flag']
        capital = data[0]['capital']
        continent = data[0]['region']
        text = f"{country} is located in {continent}. The capital of {country} is {capital} and they have a population of about {population}."

        dict1 = {'info': text, 'flag': flag}
        return dict1

if __name__ == '__main__':
    obj = Countries()
    data = obj.country_info(input())
    print(data)







