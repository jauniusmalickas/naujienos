import feedparser

from flask import Flask, render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route("/")
@app.route("/<provider>")

def get_news(provider='bbc'):
    feed = feedparser.parse(RSS_FEEDS[provider])
    #first_article = feed['entries'][0]
    articles=feed['entries']
    if articles:
        return render_template('home.html', provider=provider, articles=articles)
    else:
        return "no news still!"
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)