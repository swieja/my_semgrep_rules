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

```bash
column -s, -t < /home/rtz/github_vuln_research/my_semgrep_rules/repos_report.csv | less -#2 -N -S 


python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_list_of_repos.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/java_repos -r /home/rtz/github_vuln_research/my_semgrep_rules/java_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/java_semgrep_results.txt -c /home/rtz/github_vuln_research/my_semgrep_rules/results.csv


python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/list_of_repos_php.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/repos_dir -r /home/rtz/github_vuln_research/my_semgrep_rules/php_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/php_semgrep_results.txt -c /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/results.csv


python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/list_of_repos_python.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/repos_dir -r /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules -s /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/python_semgrep_results.txt -c /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/results.csv


#count the number of occurrences
cd /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos
fgrep home.rtz.github_vuln_research.my_semgrep_rules. php/php_semgrep_results.txt_textpattern.textpattern.txt > lol.txt
./count_words.sh lol.txt > asd.txt 
code asd.txt
```



```bash
cd /home/rtz/github_vuln_research/semgrep-rules/python ; find `pwd` -name *.yaml  | tee /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/full_list.txt > /dev/null
python3 /home/rtz/github_vuln_research/my_semgrep_rules/remove_unwanted_rules.py /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/rule_list.txt | tee /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/list.txt  > /dev/null
while read p ; do cp $p /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/; done < /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/list.txt 
rm /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/full_list.txt /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules/rule_list.txt 
cd /home/rtz/github_vuln_research/my_semgrep_rules/python_semgrep_rules
```