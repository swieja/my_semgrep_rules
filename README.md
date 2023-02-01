# Project notes
semgrep command to run all rules from `java` directory to scan vespa source code
`python3 -m semgrep --config /home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/vespa`


testing:
`python3 -m semgrep --config /home/rtz/github_vuln_research/my_semgrep_rules/java/find-sql-string-concatenation.yaml /home/rtz/github_vuln_research/vespa`


classic rce \
seralization \
lfi \
ssrf \
sqli

## general commands
```bash
column -s, -t < /home/rtz/github_vuln_research/my_semgrep_rules/repos_report.csv | less -#2 -N -S 


python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/list_of_repos_java.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/repos_dir -r /home/rtz/github_vuln_research/my_semgrep_rules/java_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/java_semgrep_results -c /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/results.csv


python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/list_of_repos_php.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/repos_dir -r /home/rtz/github_vuln_research/my_semgrep_rules/php_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/php_semgrep_results -c /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/results.csv

python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/list_of_repos_csharp.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/repos_dir -r /home/rtz/github_vuln_research/my_semgrep_rules/csharp_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/php_semgrep_results -c /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/results.csv


python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/list_of_repos_python.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/repos_dir -r /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/python_semgrep_results -c /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/results.csv

python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.p    y -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/list_of_repos_go.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/repos_dir -r /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go_semgrep_results -c /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/results.csv

python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/list_of_repos_js.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/repos_dir -r /home/rtz/github_vuln_research/my_semgrep_rules/js_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/js_semgrep_results -c /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/results.csv


#count the number of occurrences to remove most likely fps
cd /home/rtz/github_vuln_research/my_semgrep_rules/
mkdir /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go
mv go_semgrep* /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go
cd /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go
fgrep home.rtz.github_vuln_research.my_semgrep_rules. * > lol.txt
/home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/count_words.sh lol.txt > asd.txt 
code asd.txt
```


## generate rules
```bash
cd /home/rtz/github_vuln_research/semgrep-rules/python ; find `pwd` -name *.yaml  | tee /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/full_list.txt > /dev/null
python3 /home/rtz/github_vuln_research/my_semgrep_rules/remove_unwanted_rules.py /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/rule_list.txt | tee /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/list.txt  > /dev/null
while read p ; do cp $p /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/; done < /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/list.txt 
rm /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/full_list.txt /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/rule_list.txt 
cd /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules
```


## modified repo finding tool to add desc for each repo
I had to modify the script to add description for each repo so it better to filter which is usually needed anyway
```
python3 find_repos_and_add_desc.py -q "NOT in:descritpion library NOT in:readme exercise stars:500..5000 language:Java" -f java_repos_semgrep.txt -s 10000
```