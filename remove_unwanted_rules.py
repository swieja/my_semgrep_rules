#Removing unwanted rules (xss,csrf, tls etc) and the ones that have low impact AND low likelihood
import sys
import re

with open(sys.argv[1],"r")as file_list:
    file_names = file_list.readlines()

file_names = [file_name.strip() for file_name in file_names]

blacklist_keywords = [
    "xss","csrf","redirect","category: correctness","category: best-practice",
    "this rule has been deprecated","improper encoding or escaping of output",
    "cryptographic failures","improper certificate valbrokation","insecure-resteasy-deserialization",
    "incorrect type conversion or cast","inadequate encryption strength"]

for file_name in file_names: 
    
    with open(file_name, "r") as somefile:
        file_contents = somefile.read()
        #if "xss" not in file_contents.lower():
        if not any (string in file_contents.lower() for string in blacklist_keywords):
            if not (re.search(r'likelihood: LOW', file_contents) and re.search(r'impact: LOW', file_contents)):
                print(file_name)