import subprocess
from time import sleep


stack = ["Java","Ruby","PHP","Go","csharp","Python"]

for lang in stack:
    for i in range (1000,12001,5000):
        if lang == "csharp":
            save = lang
            lang = "C#"
            cmd = f"python3 /home/rtz/github_vuln_research/my_semgrep_rules/find_repos_and_add_desc.py -q \"NOT in:descritpion library NOT in:readme exercise stars:{i}..{i+2000} language:{lang} created:>2017-01-01 sort:updated\" -f /home/rtz/github_vuln_research/my_semgrep_rules/{save}_all/{save}_repos_list_semgrep.txt -s 20000"
            lang = save
            subprocess.run(cmd,shell=True)
            sleep(30)
        else:
            cmd = f"python3 /home/rtz/github_vuln_research/my_semgrep_rules/find_repos_and_add_desc.py -q \"NOT in:descritpion library NOT in:readme exercise stars:{i}..{i+2000} language:{lang} created:>2017-01-01 sort:updated\" -f /home/rtz/github_vuln_research/my_semgrep_rules/{lang}_all/{lang}_repos_list_semgrep.txt -s 20000"            
            subprocess.run(cmd,shell=True)
            sleep(30)