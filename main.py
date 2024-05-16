import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY')
WEBSHARE_USER = os.environ.get('WEBSHARE_USER')
WEBSHARE_PASS = os.environ.get('WEBSHARE_PASS')

def get_proxy():
    return f"http://{WEBSHARE_USER}:{WEBSHARE_PASS}@38.154.227.167:5868"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/searchPlayerTag', methods=['POST'])
def search():
    if "playerTag" not in request.json:
        return "One or more required payloads missing"
    
    PLAYER_TAG = request.json['playerTag']

    url = f'https://api.brawlstars.com/v1/players/%23{PLAYER_TAG}'

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    proxy = get_proxy()

    if not proxy:
        return "Failed to retrieve proxy"

    proxies = {
        'http': proxy,
        'https': proxy
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxies)

        print(f"Response: {response.json()}")
        print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            player_info = response.json()
            return jsonify(player_info)
        else:
            return "Player not found"
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to communicate with API. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)

