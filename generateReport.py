import sys
import os 
import requests
import json


try: 
    ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
except KeyError:
    print("No GITHUB_ACCESS_TOKEN environment variable.")
    sys.exit(1)

BASE_URL = " https://api.github.com/search"

s = requests.Session()

repoListPath = "/home/rtz/github_vuln_research/my_semgrep_rules/custom_list_of_repos.txt"


with open(repoListPath, "r") as f:
    repoList = f.read().split("\n")


# while read p; do 
#     a=$(echo $p |awk -F "/" '{print $5}'); git clone $p.git;python3 -m semgrep --config=auto $a  | tee /home/rtz/github_vuln_research/semgrep_results/$a.txt ; python3 -m semgrep --config "p/r2c-security-audit" $a | tee -a /home/rtz/github_vuln_research/semgrep_results/$a.txt ; rm -rf $a ; sleep 90
# done < /home/rtz/github_vuln_research/repoList.txt



for i in repoList:
    fullNameRepo = '.'.join(i.rsplit("/",2)[-2:])
    os.system("python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java | tee ")