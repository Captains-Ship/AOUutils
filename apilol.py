from flask import *
from threading import Thread
import json
import requests

app = Flask('')


@app.route('/')
def owo():
    return render_template('main.html')


@app.route('/api')
def getapiversions():
    latestapi = [
        'v1'
    ]
    apis = [
        'v1'
    ]
    milk = f"<A href=\"/api/{latestapi[0]}\">Latest ({latestapi[0]})</a><br><br>"
    for api in apis:
        milk = milk + f"\n<A href=\"/api/{api}\">{api}</a><br><br>"
    return milk


def validate_dev_token(token):
    if token == 'CQDgrhUrVQVKHXag':
        return True
    else:
        return False


@app.route('/api/dev')
async def dev():
    token = 'CQDgrhUrVQVKHXag'
    key = request.args.get('key')
    if key is None:
        return 'Missing API Key'
    else:
        if key == token:
            return "pog"
        else:
            return 'invalid API key'


@app.route('/api/dev/test')
async def dev_test():
    key = request.args.get('key')
    if validate_dev_token(key) is True:
        return 'im gonna milk you'
    else:
        return 'Invalid API key'


@app.route('/api/v1')
def main():
    return render_template('index.html')


@app.route('/api/v1/membercount')
def mc():
    with open('memcount.json', 'r') as f:
        mclol = json.load(f)
        return jsonify(mclol)


@app.route('/api/v1/currency/<ide>')
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


@app.route('/api/v1/currency')
async def osdughfdsig():
    with open('cur.json', 'r') as f:
        cur = json.load(f)
        return cur


@app.errorhandler(500)
async def _500(h=None):
    h = h if h is not None else "No error provided to handler"
    return "An internal server error has occured! please report this to a dev!" + f"<br><br>{h}"


@app.route('/test')
async def test():
    return """
    <body style="background-color: #111111"> 
        <h1 style="color:#FFFFFF">
            Testing Grounds (get out)
        </h1>
    <script>
        alert('out or im gonna milk you')
    </script>
    </body>
    """


@app.errorhandler(404)
async def _404(h=None):
    return render_template('404.html')


@app.route('/api/v1/latest')
async def getlatestaou():
    try:
        request_instance = requests.get('https://angxl.xyz/api/allofus/getLatest')
        request_content = str(request_instance.content)
    except:
        return 'Unable to access api.'
    try:
        request_is_json = json.loads(request_content)
        return request_is_json
    except:
        return request_content


@app.route('/join')
async def join():
    return render_template('invite.html')


def run():
    app.run(host="127.0.0.1", port=8080)


def start():
    server = Thread(target=run)
    server.start()


