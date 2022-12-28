from flask import Flask, request, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)
result = ""

@app.route('/', methods=['GET'])
def index():
    return 'Hello, week 15'

@app.route("/publication", methods=['GET'])
def publication():
    try:
        year = request.args
        year = year["year"]  #from template

        if int(year) <= 2021 and int(year) >= 2000:
            html = requests.get("http://monet.skku.edu/?page_id=3550").text
            bsObject = BeautifulSoup(html, 'html.parser')
            info = bsObject.select('.container>div>div>div>div')

            i = 2021
            for item in info:
                selectedInfo = item.select('article>div>header>h2')
                if i==int(year):
                    break;
                else:
                    i -= 1

            result = []
            #print(selectedInfo)

            for element in selectedInfo:
                #print(element.text)
                result.append(element.text)

            result.reverse()

            #print(result)
        else:
            result = ["There is no publication list for that year or you have entered it incorrectly."]
        return render_template('publication.html', result = result)
    except:
        if year == "" :
            result = ["There is no publication list for that year or you have entered it incorrectly."]
            return render_template('publication.html', result = result)
        return render_template('publication.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
