from flask import Flask, request, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)
result = ""

@app.route('/', methods=['GET'])
def index():
    return 'Hello, week 15'

@app.route("/covid", methods=['GET'])
def covid():
    try:
        html = requests.get("https://covid19.who.int/table").text
        bsObject = BeautifulSoup(html, 'html.parser')
        list = bsObject.select('.tbody>div>div>div')
        topFivelist = []
        names = []
        tcases = []
        tdeaths = []
        cnt = 0
        for item in list:
            if cnt >= 2 and cnt < 7:
                topFivelist+=item
            cnt += 1
        for item in topFivelist:
            # .find('div', {"class" : "sc-AxjAm sc-qXRQq bJEXVx"}).find('span')
            tmp = item.select('.column_name>div>span')
            tmp2 = item.select('.column_Cumulative_Confirmed>div>div>div')
            tmp3 = item.select('.column_Cumulative_Deaths>div')
            if tmp != []:
                names.append(tmp[0].text)
            if tmp2 != []:
                tcases.append(tmp2[0].text)
            if tmp3 != []:
                tdeaths.append(tmp3[0].text)
        #print(names)
        #print(tcases)
        #print(tdeaths)

        result = []
        for i in range(5):
            result.append(names[i])
            result.append(tcases[i])
            result.append(tdeaths[i])
        return render_template('covid.html', result = result)
    except:
        return render_template('covid.html', result = 'ERROR: No search results')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
