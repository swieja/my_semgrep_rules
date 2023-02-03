import subprocess


stack = ["Java","Ruby","PHP","Go","csharp","Python"]

for lang in stack:
    for i in range (500,7000,501):
        if lang == "csharp":
            save = lang
            lang = "C%23"
            cmd = f"python3 /home/rtz/github_vuln_research/my_semgrep_rules/find_repos_and_add_desc.py -q \"NOT in:descritpion library NOT in:readme exercise stars:{i}..{i+500} language:{lang} created:>2017-01-01 sort:updated\" -f /home/rtz/github_vuln_research/my_semgrep_rules/{save}_all/{save}_repos_list_semgrep.txt -s 20000"
            lang = save
            print(cmd)
        else:
            cmd = f"python3 /home/rtz/github_vuln_research/my_semgrep_rules/find_repos_and_add_desc.py -q \"NOT in:descritpion library NOT in:readme exercise stars:{i}..{i+500} language:{lang} created:>2017-01-01 sort:updated\" -f /home/rtz/github_vuln_research/my_semgrep_rules/{lang}_all/{lang}_repos_list_semgrep.txt -s 20000"            
            print(cmd)