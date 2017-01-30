import feedparser
import json 
import urllib
from urllib.request import urlopen

from flask import Flask, render_template, request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/most-popular'}

#using GET method to get feeds provider from URL like ?provider=bbc
@app.route("/")
def get_news():
    query = request.args.get('provider')
    if not query or query.lower() not in RSS_FEEDS:
        provider ='bbc'
    else:
        provider = query.lower()

    weather = get_weather("London,UK")
    feed = feedparser.parse(RSS_FEEDS[provider])
    articles=feed['entries']
    if articles:
        return render_template('home.html', provider=provider, articles=articles, weather=weather)
    else:
        return "no news still!"

def get_weather(query):
    args = {"q": "", "units": "metric", "appid": "bbaffd18fad8101c96023d9a4c248018"}
    base_url = "http://api.openweathermap.org/data/2.5/weather?{}"
       
    query = urllib.parse.quote(query) 
    args.update(q=query)

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