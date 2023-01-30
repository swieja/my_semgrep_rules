import sys
import re
import requests
import json
import subprocess
from os import environ
from time import sleep
from argparse import ArgumentParser, RawTextHelpFormatter


try: 
    ACCESS_TOKEN = environ["GITHUB_ACCESS_TOKEN"]
except KeyError:
    print("No GITHUB_ACCESS_TOKEN environment variable.")
    sys.exit(1)

API_URL = "https://api.github.com/repos"

def getFindingCount(stderr):
    match = re.search(r"Ran.*findings.",str(stderr, 'utf-8'))
    if match:
        findingCount = re.findall(r"files.*?(\d+)\s",match.group())
        return findingCount[0]
    
def get_args(prog):
    helpm = f"Example: \r\n{prog} -l ~/list_of_repos.txt -d ~/java_cloned_repos_dir -r ~/semgrep_java_rules_dir -s ~/java_semgrep_results -c ~/report.csv"
    parser = ArgumentParser(epilog=helpm,formatter_class=RawTextHelpFormatter)
    parser.add_argument('-l','--list',dest="listOfRepos",action='store',type=str,required=True)
    parser.add_argument('-d','--directory',dest="directoryRepos",action='store',type=str,required=True)
    parser.add_argument('-r','--rules',dest="directoryRules",action='store',type=str,required=True)
    parser.add_argument('-s','--save',dest="semgrepResults",action='store',type=str,required=True)
    parser.add_argument('-c','--csv',dest="csvStore",action='store',type=str,required=True)



if __name__ == "__main__":
    args = get_args(sys.argv[0])
    s = requests.Session()
    
    filePath = args.listOfRepos
    with open(filePath, "r") as f:
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
        #cmd = f"git clone {URL} /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}"
        cmd = f"git clone {URL} {args.directoryRepos}/{fullNameRepo}"
        subprocess.run(cmd,shell=True,capture_output=False)

        #running semgrep, saving results and basic repo info
        #cmd = f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}"
        cmd = f"python3 -m semgrep --config={args.directoryRules} {args.directoryRepos}/{fullNameRepo}"
        output = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr = output.communicate()
        with open(f"{args.semgrepResults}_{fullNameRepo}.txt","a") as file:
            file.write(str(stdout,'utf-8'))

        # get amount of findings 
        findingCount = getFindingCount(stderr)
        

        #save to csv
        with open(f"{args.csvStore}","a") as file:
            file.write(f"{URL},Java,{str(data['stargazers_count'])},{str(data['size'])},{str(findingCount)}\n")

        cmd = f"rm -rf {args.directoryRepos}/{fullNameRepo}"
        subprocess.run(cmd,shell=True)

        print(f"{URL},Java,{str(data['stargazers_count'])},{str(data['size'])},{str(findingCount)}\n")
        sleep(60)
        