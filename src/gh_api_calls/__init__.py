import requests
import subprocess
import json

def get_commits(user, repo,api_key):
    url = f'https://api.github.com/repos/{user}/{repo}/commits'
    
    res = json.loads(subprocess.Popen(f"curl {url} -H \"Authorization: Bearer {api_key}\"", shell=True, stdout=subprocess.PIPE).stdout.read())
    return len(res)
