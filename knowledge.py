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



if __name__ == '__main__':
    know_obj = Knowledge('d35c29eecae9b60ada2a0565f75ec5b9')
    data = know_obj.get_location()
    print(data)




