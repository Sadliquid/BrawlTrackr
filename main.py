import requests, os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

load_dotenv()

API_KEY = os.environ.get('API_KEY')

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

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        player_info = response.json()
        return jsonify(player_info)
    else:
        return "Player not found"

if __name__ == '__main__':
    app.run(debug=True)
