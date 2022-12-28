from flask import Flask, request, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)
result = ""


@app.route('/', methods=['GET'])
def index():
    return 'Hello, week 15'

@app.route("/finance", methods=['GET'])
def finance():
    try:
        html = requests.get("https://www.investing.com/indices/nasdaq-composite").text
        bsObject = BeautifulSoup(html, from_encoding='en')
        index = bsObject.find('span', {"class":"text-2xl"})
        result = "NASDAQ index is Now " + index.text
        return render_template('finance.html', result = result)
    except:
        return render_template('finance.html', result = 'ERROR: No search results')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
