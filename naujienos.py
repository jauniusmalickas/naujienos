import feedparser

from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route("/")
@app.route("/<provider>")

def get_news(provider='bbc'):
    feed = feedparser.parse(RSS_FEEDS[provider])
    first_article = feed['entries'][0]
    if first_article: 
        return """<html>
            <body>
                <h1>Headlines </h1>
                <b> {0} </b><br/>
                <i> {1} </i><br/>
                <p> {2} </p><br/>
            </body>
        </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))
    else:
        return "no news still!"
    
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)