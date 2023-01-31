# Project notes
semgrep command to run all rules from `java` directory to scan vespa source code
python3 -m semgrep --config /home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/vespa


testing:
python3 -m semgrep --config /home/rtz/github_vuln_research/my_semgrep_rules/java/find-sql-string-concatenation.yaml /home/rtz/github_vuln_research/vespa 


classic rce \
seralization \
lfi \
ssrf \
sqli \ 


column -s, -t < /home/rtz/github_vuln_research/my_semgrep_rules/repos_report.csv | less -#2 -N -S 


python3 /home/rtz/github_vuln_research/my_semgrep_rules/generateReport.py -l /home/rtz/github_vuln_research/my_semgrep_rules/custom_list_of_repos.txt -d /home/rtz/github_vuln_research/my_semgrep_rules/java_repos -r /home/rtz/github_vuln_research/my_semgrep_rules/java -s /home/rtz/github_vuln_research/my_semgrep_rules/java_semgrep_results.txt -c /home/rtz/github_vuln_research/my_semgrep_rules/results.csv

