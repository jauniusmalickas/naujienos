from flask import Flask

app = Flask(__name__)
@app.route("/")
def get_newa():
    return "no news still!"

if __name__ == '__main__':
    app.run(port=5000, debug=True)