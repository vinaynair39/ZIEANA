import requests
import json
import feedparser
import time
import datetime
import time
class Knowledge:

    def __init__(self, darksky_token, country_code='in'):
        self.darksky_api_token = darksky_token
        self.country_code = country_code

    def get_ip(self):
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']

    def get_location(self):
        # get location
        location_req_url = f"http://freegeoip.net/json/{self.get_ip()}"
        r = requests.get(location_req_url)
        location_obj = json.loads(r.text)

        lat = location_obj['latitude']
        lon = location_obj['longitude']

        return {'lat': lat, 'lon': lon}

    def find_weather(self):
        loc_obj = self.get_location()

        lat = loc_obj['lat']
        lon = loc_obj['lon']

        weather_req_url = f"https://api.darksky.net/forecast/{self.darksky_api_token}/{lat},{lon}?units=si"
        r = requests.get(weather_req_url)
        weather_json = json.loads(r.text)

        temperature = int(weather_json['currently']['temperature'])
        current_forecast = weather_json['currently']['summary']
        daily_forecast = weather_json['hourly']['summary']
        weekly_forecast = weather_json['daily']['summary']
        icon = weather_json['currently']['icon']
        wind_speed = int(weather_json['currently']['windSpeed'])

        return {'temperature': temperature,
                'icon': icon,
                'windSpeed': wind_speed,
                'current_forecast': current_forecast,
                'daily_forecast': daily_forecast,
                'weekly_forecast': weekly_forecast
                }

    def get_news(self):
        ret_headlines = []
        feed = feedparser.parse("https://news.google.com/news?ned=%s&output=rss" % self.country_code)
        for post in feed.entries[1:4]:
            ret_headlines.append(post.title)

        return ret_headlines

    def current_datetime(self):
        full_time = time.strftime('%d  %B,  %I %M %p').lstrip('0')
        leading_removed = [i.lstrip('0') for i in full_time]     # to remove the leading 0's
        full_time = ''.join(leading_removed)     # to convert the list to a string
        return full_time

    def current_date(self):
        full_date = time.strftime('%d  %B,  %Y').lstrip('0')
        return full_date

    def current_time(self):
        full_time = time.strftime('%I %M %p').lstrip('0')
        return full_time

    def distance(self, origin, destination):
        key = 'AIzaSyB-tZAt2uCt2PzGjn_jNWFBjgT17nR47MY'
        r = requests.get(f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={key}')
        data = json.loads(r.text)
        distance = data['rows'][0]['elements'][0]['distance']['text']
        time = data['rows'][0]['elements'][0]['duration']['text']

        text = f'The distance is {distance}. It will take you approximately {time} to reach there.'

        return text

    def lat_lng(self, address):
        key = 'AIzaSyAV_ErAt2TjNSFKE74cE6MKVafAiCr4nSs'
        r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}')
        data = json.loads(r.text)
        # print(json.dumps(data, indent=2))
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']

        return lat, lng

    def ola_fare(self, origin_lat, origin_lng, destination_lat, destination_lng):

        r = requests.get(f'https://devapi.olacabs.com/v1/products?pickup_lat={origin_lat}&pickup_lng={origin_lng}&drop_lat={destination_lat}&drop_lng={destination_lng}&service_type=p2p')
        data = json.loads(r.text)
        print(json.dumps(data, indent=2))

if __name__ == '__main__':
    know_obj = Knowledge('d35c29eecae9b60ada2a0565f75ec5b9')
    origin_lat, origin_lng = know_obj.lat_lng('airoli plaza b sector 16, airoli, navi mumbai')
    destination_lat, destination_lng = know_obj.lat_lng('pillai panvel')
    know_obj.ola_fare(origin_lat, origin_lng, destination_lat, destination_lng)








