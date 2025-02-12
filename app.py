import flask
from flask import request, render_template, jsonify
import gh_api_calls as gac
from dotenv import load_dotenv

import os, json
load_dotenv()

GH_API_KEY = os.getenv('GH_API_KEY')
AUTH_KEY = os.getenv('AUTH_KEY')

app = flask.Flask(__name__)

config = {}
with open('config.json') as f:
    config = json.load(f)

def check_auth(key):
    return key == AUTH_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/commits')
def commits():
    if not check_auth(request.args.get('auth_key')):
        return "Unauthorized", 401
    sum = 0
    if request.args.get('repo'):
        return str(gac.get_commits(config["user"],request.args.get('repo'),GH_API_KEY))
    for repo in config['repos']:
        sum += gac.get_commits(config["user"],repo,GH_API_KEY)
    return jsonify({"commits": sum})
