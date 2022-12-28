from flask import Flask, request, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)


@app.route('/', methods= ['GET'])
def index():
    return render_template('index.html')

@app.route("/finance", methods=['GET'])
def finance():
    try:
        html = requests.get("https://www.investing.com/indices/nasdaq-composite").text
        bsObject = BeautifulSoup(html, from_encoding='en')
        index = bsObject.find('span', {"class":"text-2xl"})
        result = "NASDAQ index is Now " + index.text
        return render_template('extend_finance.html', result = result)
    except:
        return render_template('extend_finance.html', result = 'ERROR: No search results')

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
        return render_template('extend_covid.html', result = result)
    except:
        return render_template('extend_covid.html', result = 'ERROR: No search results')

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
        return render_template('extend_publication.html', result = result)
    except:
        if year == "" :
            result = ["There is no publication list for that year or you have entered it incorrectly."]
            return render_template('extend_publication.html', result = result)
        return render_template('extend_publication.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
