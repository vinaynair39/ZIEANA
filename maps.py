import json
import requests
from knowledge import Knowledge




class Maps:

    def __init__(self):
        self.know = Knowledge()

    def direction(self):
        loc_obj = self.know.get_location()
        lat = loc_obj['lat']
        long = loc_obj['lon']
        key = 'AIzaSyBKebb2eYTVYHYQcWuhr2DMi_YFcq - bJdY'
        destination = "pillai panvel"
        r = requests.get(f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat},{long}&destinations={destination}&key={key}')
        data = json.loads(r.text)
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    obj = Maps()
    obj.direction()