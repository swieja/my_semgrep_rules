import subprocess
import requests
import json
import sys
import re
import os 

from time import sleep
from argparse import ArgumentParser, RawTextHelpFormatter


try: 
    ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
except KeyError:
    print("No GITHUB_ACCESS_TOKEN environment variable.")
    sys.exit(1)

API_URL = "https://api.github.com/repos"

def getFindingCount(stderr):
    match = re.search(r"Ran.*findings.",str(stderr, 'utf-8'))
    if match:
        findingCount = re.findall(r"files.*?(\d+)\s",match.group())
        return findingCount[0]
    
1

def get_args(prog):
    helpm = f"Example: \r\n{prog} -l ~/list_of_repos.txt -d ~/java_cloned_repos_dir -r ~/semgrep_java_rules_dir -s ~/java_semgrep_results -c ~/report.csv"
    parser = ArgumentParser(epilog=helpm,formatter_class=RawTextHelpFormatter)
    parser.add_argument('-l','--list',dest="listOfRepos",action='store',type=str,required=True)
    parser.add_argument('-d','--directory',dest="directoryRepos",action='store',type=str,required=True)
    parser.add_argument('-r','--rules',dest="directoryRules",action='store',type=str,required=True)
    parser.add_argument('-s','--save',dest="semgrepResults",action='store',type=str,required=True)
    parser.add_argument('-c','--csv',dest="csvStore",action='store',type=str,required=True)
    return parser.parse_args()

def checkArgs():
    args = get_args(sys.argv[0])

    if not os.path.exists(args.directoryRepos):
        print(f"Didn't find {args.directoryRepos}, creating it")
        os.makedirs(args.directoryRepos)
    elif os.path.exists(args.directoryRepos):
        pass
    else:
        print("Something went wrong, permission issues?")
        sys.exit()
    
    if not os.path.exists(args.listOfRepos):
        print(f"Didn't find {args.listOfRepos}, provide a valid path to list of repos.")
        sys.exit()

    if not os.path.exists(args.directoryRules):
        print(f"Didn't find {args.directoryRules}, provide a valid path to directory with semgrep rules.")
        sys.exit()
    elif os.path.isdir(args.directoryRules):
        if not os.listdir(args.directoryRules):
            print(f"Directory {args.directoryRules} is empty.")
            sys.exit()
    else:
        print(f"{args.directoryRules} is not a directory.")
        sys.exit()
    

    if not os.path.exists(args.semgrepResults):
        print(f"Didn't find {args.semgrepResults}, creating it")
        os.makedirs(args.semgrepResults)
    elif os.path.exists(args.semgrepResults):
        pass
    else:
        print("Something went wrong, permission issues?")
        sys.exit()

    if not os.access(args.semgrepResults,os.W_OK):
        print(f"Current user doesn't have write access to {args.semgrepResults}.")
        sys.exit()

    if not os.access(os.path.dirname(args.csvStore), os.W_OK):
        print(f"The current user doesn't have write access to {os.path.dirname(args.csvStore)}.")
        sys.exit()   
    
    

if __name__ == "__main__":
    args = get_args(sys.argv[0])
    s = requests.Session()

    checkArgs()
    
    with open(args.listOfRepos, "r") as f:
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
        print(f"Cloning the repo: {URL}: ")
        cmd = f"git clone {URL} {args.directoryRepos}/{fullNameRepo}"
        subprocess.run(cmd,shell=True,capture_output=False)

        #running semgrep, saving results and basic repo info
        #cmd = f"python3 -m semgrep --config=/home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/my_semgrep_rules/java_repos/{fullNameRepo}"
        print(f'''Running semgrep on {fullNameRepo} located in {args.directoryRepos},
        directory with rules: {args.directoryRules} ,
        saving semgrep results to: {args.semgrepResults}_{fullNameRepo}.txt.
        ''')
        
        print(f"python3 -m semgrep --config={args.directoryRules} {args.directoryRepos}/{fullNameRepo}")
        cmd = f"python3 -m semgrep --config={args.directoryRules} {args.directoryRepos}/{fullNameRepo}"
        output = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr = output.communicate()
        #print(str(stdout,'utf-8'))
        print(str(stderr,'utf-8'))
        with open(f"{args.semgrepResults}_{fullNameRepo}.txt","a") as file:
            file.write(str(stdout,'utf-8'))

        # get amount of findings 
        findingCount = getFindingCount(stderr)
        
        print(f"Saving csv: {args.csvStore}")
        #save to csv
        with open(f"{args.csvStore}","a") as file:
            file.write(f"{URL},PHP,{str(data['stargazers_count'])},{str(data['size'])},{str(findingCount)}\n")
        
        print(f"Deleting the directory: {args.directoryRepos}/{fullNameRepo}")
        cmd = f"rm -rf {args.directoryRepos}/{fullNameRepo}"
        subprocess.run(cmd,shell=True)

        print(f"{URL},Java,{str(data['stargazers_count'])},{str(data['size'])},{str(findingCount)}\n")
        sleep(15)
        