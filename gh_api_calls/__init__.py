import requests
import subprocess
import json, re

def extract_page_number(link_header):
    match = re.search(r'.*"next".*page=(\d{1,4}).*"last".*', link_header)
    return match.group(1) if match else None

def get_commits(user, repo,api_key):
    url = f'https://api.github.com/repos/{user}/{repo}/commits?per_page=1'
    
    res = subprocess.Popen(f"curl -I -k {url} -H \"Authorization: Bearer {api_key}\"", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')   
    page_number = extract_page_number(res)

    return int(page_number)
