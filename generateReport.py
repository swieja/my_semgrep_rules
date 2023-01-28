import sys
import os 
import requests
from time import sleep


try: 
    ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
except KeyError:
    print("No GITHUB_ACCESS_TOKEN environment variable.")
    sys.exit(1)

repoListPath = "/home/rtz/github_vuln_research/my_semgrep_rules/custom_list_of_repos.txt"


with open(repoListPath, "r") as f:
    repoList = f.read().split("\n")


# while read p; do 
#     a=$(echo $p |awk -F "/" '{print $5}'); git clone $p.git;python3 -m semgrep --config=auto $a  | tee /home/rtz/github_vuln_research/semgrep_results/$a.txt ; python3 -m semgrep --config "p/r2c-security-audit" $a | tee -a /home/rtz/github_vuln_research/semgrep_results/$a.txt ; rm -rf $a ; sleep 90
# done < /home/rtz/github_vuln_research/repoList.txt

for URL in repoList:
    fullNameRepo = '.'.join(URL.rsplit("/",2)[-2:])
    os.system(f"git clone -v --progress {URL} /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")
    os.system(f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo} > /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/semgrep_resutl_{fullNameRepo}.txt 2>&1")
    os.system(f"rm -rf /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")
    
    # os.system(f"git clone -v --progress {URL} /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")
    # os.system(f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/semgrep_resutl_{fullNameRepo}/ | tee /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/semgrep_resutl_{fullNameRepo} ; rm -rf /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}")

    sys.exit(1)