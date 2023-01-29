import sys
import re
import requests
import json
import subprocess
from os import environ
from time import sleep

def getFindingCount(stderr):
    match = re.search(r"Ran.*findings.",str(stderr, 'utf-8'))
    if match:
        findingCount = re.findall(r"files.*?(\d+)\s",match.group())
        return findingCount[0]

try: 
    ACCESS_TOKEN = environ["GITHUB_ACCESS_TOKEN"]
except KeyError:
    print("No GITHUB_ACCESS_TOKEN environment variable.")
    sys.exit(1)


API_URL = "https://api.github.com/repos"
s = requests.Session()

try: 
    ACCESS_TOKEN = environ["GITHUB_ACCESS_TOKEN"]
except KeyError:
    print("No GITHUB_ACCESS_TOKEN environment variable.")
    sys.exit(1)

repoListPath = "/home/rtz/github_vuln_research/my_semgrep_rules/custom_list_of_repos.txt"


with open(repoListPath, "r") as f:
    repoList = f.read().split("\n")

headers = {
    "Accept" : "application/vnd.github+json",
    "Authorization" : f"Bearer {ACCESS_TOKEN}",
    "X-GitHub-Api-Version":"2022-11-28"}


for URL in repoList:

    #get stars and size
    repoName = '/'.join(URL.rsplit("/",2)[-2:])
    r = s.get(f"{API_URL}/{repoName}",headers=headers)
    data =json.loads(r.text)

    fullNameRepo = '.'.join(URL.rsplit("/",2)[-2:])

    # cloning the repo
    cmd = f"git clone -v --progress {URL} /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}"
    subprocess.run(cmd,shell=True,capture_output=False)

    #running semgrep, saving results and basic repo info
    cmd = f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}"
    output = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = output.communicate()
    with open(f"/home/rtz/github_vuln_research/my_semgrep_rules/java_repos/semgrep_results_{fullNameRepo}","a") as file:
        file.write(str(stdout,'utf-8'))

    # get amount of findings 
    findingCount = getFindingCount(stderr)
    

    #save to csv
    with open("/home/rtz/github_vuln_research/my_semgrep_rules/repos_report.csv","a") as file:
        file.write(f"{URL},Java,{str(data['stargazers_count'])},{str(data['size'])},{str(findingCount)}\n")

    sleep(60)
    #sys.exit(1)