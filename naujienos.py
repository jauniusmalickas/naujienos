import feedparser
import json 
import urllib
from urllib.request import urlopen

from flask import Flask, render_template, request

app = Flask(__name__)

DEFAULTS = {'provider':'bbc', 'city':'Vilnius, LT'}

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/most-popular'}

#using GET method to get feeds provider from URL like ?provider=bbc
@app.route("/")
def home():
    provider = request.args.get('provider')
    if not provider or provider.lower() not in RSS_FEEDS:
        provider =DEFAULTS['provider']

    articles = get_news(provider.lower())

    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    
    weather = get_weather(city)

    if articles:
        return render_template('home.html', provider=provider, articles=articles, weather=weather)
    else:
        return "no news still!"


#get_news procedure based on provider paramater
def get_news(provider):
    
    feed = feedparser.parse(RSS_FEEDS[provider])
    return feed['entries']
    
#procedure to retrieve weather information with query parameter as city and country
def get_weather(city):
    args = {"q": "", "units": "metric", "appid": "bbaffd18fad8101c96023d9a4c248018"}
    base_url = "http://api.openweathermap.org/data/2.5/weather?{}"
       
    city = urllib.parse.quote(city) 
    args.update(q=city)

    url = base_url.format(urllib.parse.urlencode(args))

    data = urlopen(url).read().decode('utf-8')
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
            parsed["weather"][0]["description"],
            "temperature":parsed["main"]["temp"],
            "city":parsed["name"]
        }
    return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)