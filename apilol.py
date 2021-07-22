from flask import *
from threading import Thread
from utility.utils import *
import json
from json import *
import requests

app = Flask('')


@app.route('/')
def owo():
    return render_template('main.html')


@app.route('/api')
def main():
    return render_template('index.html')


@app.route('/api/membercount')
def mc():
    with open('memcount.json', 'r') as f:
        mclol = json.load(f)
        return jsonify(mclol)


@app.route('/api/currency/<ide>')
async def uwu(ide='347366054806159360'):
    try:

        ide = str(ide)
        with open('cur.json', 'r') as f:
            cur = json.load(f)
            """
            user = cur[ide]
            ci = '✧'
            wallet = user['wallet']
            bank = user['bank']
            items = user['inventory']
            response = f'The user has {wallet}{ci} in their wallet. \nThe user has {bank}{ci} in their bank. \nThe users Items are: \n{items}'
        """
        return cur[ide]
    except:
        return 'The user doesnt have an AOUutils currency account yet!'


@app.route('/api/currency')
async def osdughfdsig():
    with open('cur.json', 'r') as f:
        cur = json.load(f)
        return cur


@app.route('/api/latest')
async def getlatestaou():
    request_instance = requests.get('https://angxl.xyz/api/allofus/getLatest')
    request_content = str(request_instance.content).replace('b\'', '').replace("'", "").replace('&nbsp;', ' ').replace(
        '<br />', '\n')
    try:
        request_is_json = json.loads(request_content)
        return request_is_json
    except:
        return request_content


def run():
    app.run(host="127.0.0.1", port=8080)


def start():
    server = Thread(target=run)
    server.start()
