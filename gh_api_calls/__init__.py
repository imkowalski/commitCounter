import requests
import subprocess
import json, re

def extract_page_number(link_header):
    match = re.search(r'.*"next".*page=(\d{1,4}).*"last".*', link_header)
    return match.group(1) if match else None

def get_commits(user, repo,api_key):
    url = f'https://api.github.com/repos/{user}/{repo}/commits?per_page=1'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    link_header = response.headers.get('Link', '')
    page_number = extract_page_number(link_header)

    return int(page_number)
