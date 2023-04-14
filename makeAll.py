import os
import sys
import urllib3
import warnings
import subprocess
from shutil import copy
from argparse import ArgumentParser, RawTextHelpFormatter

#yes I need 2147483647 libraries

warnings.filterwarnings("ignore", message="Unverified HTTPS request")


SEMGREP_GITHUB = "https://github.com/returntocorp/semgrep-rules.git"
TEMPORARY_STORAGE = "/tmp/semgrep-rules/"

    

req = urllib3.PoolManager()
res = req.request('GET','https://github.com/returntocorp/semgrep-rules')
if res.status == 404:
    sys.exit("semgrep-rules repository doesn't exist (?)")

def isCorrectnessCategory(yamlFile):
    if "category: correctness" in open(yamlFile).read():
        return True

def get_args(prog):
    helpm = f"Example \r\n{prog} -s \"/home/rtz/my-semgrep-rules/\""
    parser = ArgumentParser(epilog=helpm,formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s','--store',dest="storeRules",action='store',required=True)
    return parser.parse_args()

try:
    subprocess.check_output(['git','--version'])
except subprocess.CalledProcessError:
    print("Git is required to use this tool.")


if __name__ == "__main__":
    args=get_args(sys.argv[0])

    # check if last char is forward slash
    if args.storeRules[-1] == '/':
        userPath = args.storeRules
    else:
        userPath = args.storeRules + '/'


    cmd = ["git","clone", SEMGREP_GITHUB, TEMPORARY_STORAGE]
    try:
        subprocess.run(cmd,check=True,shell=False)
    except subprocess.CalledProcessError:
        print(f"{TEMPORARY_STORAGE} already exists.")


# Testing if paths of rules that interest me exist in the repository.
# csharp, go, java, javascript, php, python, ruby.
    for rulesPath in ["csharp", "go", "java", "javascript", "php", "python", "ruby"]:
        if not os.path.isdir(TEMPORARY_STORAGE + rulesPath):
            sys.exit(f"{TEMPORARY_STORAGE + rulesPath} doesn't exist.")
        else:
            print(f"{rulesPath} exists.")

        #creating a directory for each set of rules
        storePath = args.storeRules + rulesPath
        if not os.path.exists(storePath):
            os.makedirs(storePath)
        elif os.path.exists(storePath):
            pass
        else:
            sys.exit("Something went horribly wrong, permission issues?")

        # copy security yaml files only
        fullPath = TEMPORARY_STORAGE + rulesPath
        for root, dirs, files in os.walk(fullPath):
            for file in files:
                fullPath = os.path.join(root,file)
                if file.endswith(".yaml") and "security" in fullPath:
                    copy(fullPath,storePath)

    print(f"Rules have been successsfully stored in {args.storeRules}.")
