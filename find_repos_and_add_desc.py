import requests
import json
import sys
from os import environ,path
from time import sleep
from argparse import ArgumentParser, RawTextHelpFormatter


try: 
    ACCESS_TOKEN = environ["GITHUB_ACCESS_TOKEN"]
except KeyError:
    print("No GITHUB_ACCESS_TOKEN environment variable.")
    sys.exit(1)

BASE_URL = " https://api.github.com/search"

def get_args(prog):
    helpm = f"Example: \r\n{prog} -q \"NOT in:descritpion library NOT in:readme exercise stars:500..5000 language:Java -f java_repos_semgrep.txt -s 10000\""
    parser = ArgumentParser(epilog=helpm, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-q','--query',dest="searchquery",action='store',type=str,required=True)
    parser.add_argument('-f','--filename',dest="storedFile",action='store',type=str,required=False)
    parser.add_argument('-s','--size',dest="sizeOfRepo",action='store',type=int,required=False,default=10000)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args(sys.argv[0])

    headers = {
        "Accept" : "application/vnd.github+json",
        "Authorization" : f"Bearer {ACCESS_TOKEN}",
        "X-GitHub-Api-Version":"2022-11-28"
        }

    s = requests.Session()

    query = args.searchquery.replace("#","%23")
    r = s.get(f"{BASE_URL}/repositories?q={query}&page=1&per_page=100",headers=headers)
    
    data = json.loads(r.text)

    totalNumberOfRepos = data['total_count']
    print(f"The amount of repos based on the query: {totalNumberOfRepos}")

    # Only the first 1000 search results are available
    totalNumberOfPages = totalNumberOfRepos / 100
    totalNumberOfPages = round(totalNumberOfPages)

    print(f'''
    Github API provides only up to 1000 results for each search.
    To work around split your query into small queries which will return less than 1000 results.
    The number of pages: {totalNumberOfPages}, picking only updated top 1000 results
    ''')
    
    totalNumberOfRelevantPages = round(1 * totalNumberOfPages) if totalNumberOfPages <= 10 else 10
    print(f"Looping {totalNumberOfRelevantPages} times:")

    repoCounter = 0
    repos = {}
    #general whitelisting
    unwantedDescriptionKeywords = ["bootcamp", "bootcamps", "beginner", "beginners", "exercise" , "exercises" , "labs" , "course", "shellcode", "payload", "wrapper","installer","hacking","hacker","c2","multiplayer","player","minecraft","owasp","ffmpeg",]
    unwantedRepoOwnerName = ["microsoft","dotnet","azure","tutorial","firefox","chrome","google","hacking","hacker","c2","multiplayer","player","minecraft","metamask","duckduckgo",'apache']

    for page in range(0,totalNumberOfRelevantPages,1):
        r = s.get(f"{BASE_URL}/repositories?q={query}&page={page}",headers=headers)
        data = json.loads(r.text)
        for item in data['items']:
            repoDescription = item['description']
            repoLogin = item['html_url']
            if (item['size'] > args.sizeOfRepo):
                if not any(string in str(repoDescription).lower() for string in unwantedDescriptionKeywords):
                    if not any(string in str(repoLogin).lower() for string in unwantedRepoOwnerName):
                        repoCounter += 1
                        repos[item['html_url']] = item['description']

        sleep(10) # sleep in case of rate limit



    print(f'''
    Query used: {args.searchquery}
    \r\nFiltering repos with size over {args.sizeOfRepo}
    \r\nFound {repoCounter} repositories.
    ''')

    for key,value in repos.items():
        print(key,value)
    if args.storedFile is not None:
        if path.exists(f"{args.storedFile}"):
            with open(f"{args.storedFile}","a") as file:
                for key,value in repos.items():
                    file.write(f"{key} {value}\n")
        else:
            with open(f"{args.storedFile}","w") as file:
                for key,value in repos.items():
                    file.write(f"{key} {value}\n")
    else:
        print("Didn't provide filename argument, not saving.")
        
                
    # #remove dups and sort it alphabetically
    # finalList = list(set(repoList))
    # finalList.sort()
    # if args.storedFile is not None:
    #     if path.exists(f"{args.storedFile}"):
    #         with open(f"{args.storedFile}","a") as file:
    #             file.write('\n'.join(finalList))
    #     else: 
    #         with open(f"{args.storedFile}","w") as file :
    #             file.write('\n'.join(finalList))
    #     print(f"Results saved to {args.storedFile}")
    # else:
    #     print("Didn't provide filename argument, not saving.")