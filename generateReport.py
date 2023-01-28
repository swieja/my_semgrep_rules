import sys
import re
import requests
import json
import subprocess
from os import environ
from time import sleep


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
    #print(fullNameRepo)

    #cmd = f"git clone -v --progress {URL} /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}"
    #subprocess.run(cmd,shell=True,capture_output=False)

    cmd = f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}"
    output = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = output.communicate()
    # print(f'''
    # stdout: {stdout}
    # stderr: {stderr}
    # ''')
    with open(f"/home/rtz/github_vuln_research/my_semgrep_rules/java_repos/semgrep_results_{fullNameRepo}","a") as file:
        file.write(str(stdout,'utf-8'))

    print(str(stderr, 'utf-8'))
    # get amount of findings    
    #match = re.search(r"Ran.*findings.",str(stderr, 'utf-8'))
    match = re.search(r"Ran.*findings.",str(stderr, 'utf-8'))
    if match:
        number = re.findall(r"files.*?(\d+)\s",match.group())
        print(number[0])
    


    #os.system(f"git clone -v --progress {URL} /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")
    #os.system(f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo} > /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/semgrep_resutl_{fullNameRepo}.txt 2>&1")
    #os.system(f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")
    #os.system(f"rm -rf /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")

    
    # os.system(f"git clone -v --progress {URL} /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")
    # os.system(f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/semgrep_resutl_{fullNameRepo}/ | tee /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/semgrep_resutl_{fullNameRepo} ; rm -rf /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")

    sys.exit(1)