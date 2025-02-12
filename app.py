import flask
from flask import request, render_template, jsonify
import gh_api_calls as gac
from dotenv import load_dotenv
import os, json
import time
import threading
import anybadge

load_dotenv()

GH_API_KEY = os.getenv('GH_API_KEY')
AUTH_KEY = os.getenv('AUTH_KEY')

app = flask.Flask(__name__)

config = {}
with open('config.json') as f:
    config = json.load(f)

total_commits = 0
last_updated = 0

def check_auth(key):
    return key == AUTH_KEY

def update_commit_count():
    global total_commits, last_updated
    sum_commits = 0
    for repo in config['repos']:
        sum_commits += gac.get_commits(config["user"], repo, GH_API_KEY)
    total_commits = sum_commits
    last_updated = time.time()
    print(f"Updated total commits: {total_commits}")

def start_background_updates():
    def run_updater():
        while True:
            update_commit_count()
            time.sleep(60)

    thread = threading.Thread(target=run_updater)
    thread.daemon = True  # Allow the main program to exit even if the thread is running
    thread.start()

start_background_updates()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/commits')
def commits():
    global total_commits, last_updated
    if not check_auth(request.args.get('auth_key')):
        return "Unauthorized", 401
    
    if request.args.get('repo'):
        return str(gac.get_commits(config["user"],request.args.get('repo'),GH_API_KEY))
    
    return jsonify({"commits": total_commits})

@app.route('/img')
def image():
    global total_commits
    badge = anybadge.Badge('commits', total_commits, default_color='green')
    svg = badge.badge_svg_text
    return svg, 200, {'Content-Type': 'image/svg+xml'}
