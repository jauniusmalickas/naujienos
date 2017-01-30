import feedparser

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

    feed = feedparser.parse(RSS_FEEDS[provider])
    articles=feed['entries']
    if articles:
        return render_template('home.html', provider=provider, articles=articles)
    else:
        return "no news still!"
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)