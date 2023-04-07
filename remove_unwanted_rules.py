#Removing unwanted rules (xss,csrf,broken access control etc)
import sys
viable = []

with open(sys.argv[1],"r")as file_list:
    file_names = file_list.readlines()

file_names = [file_name.strip() for file_name in file_names]


for file_name in file_names: 
    
    with open(file_name, "r") as somefile:
        file_contents = somefile.read()
        #if "xss" not in file_contents.lower():
        if not any (string in file_contents.lower() for string in ["xss","csrf","redirect","category: correctness","category: best-practice","this rule has been deprecated","improper encoding or escaping of output"]):
            print(file_name)