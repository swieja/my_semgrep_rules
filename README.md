# Project notes
A set of scripts and stuff to utilize [repo-find](https://github.com/jkob-sec/repo-find) and semgrep stolen from [semgrep-rules](https://github.com/returntocorp/semgrep-rules) for vulnerability research in  open source projects on github. 

This requires [semgrep CLI](https://semgrep.dev/docs/getting-started/) to be installed:

testing:
`python3 -m semgrep --config /home/rtz/github_vuln_research/my_semgrep_rules/java/find-sql-string-concatenation.yaml /home/rtz/github_vuln_research/vespa`

stolen semgrep rules include:
- classic rce
- seralization
- lfi
- ssrf
- sqli

## General Use
```console
python3 generateReport.py -l text_file_with_urls_of_repos \
 -d temp_repos_directory \
 -r directory_with_rules \
 -s semgrep_results_directory \
 -c results_in_csv_format
```

For example: 
```console
python3 generateReport.py -l custom_repos/list_of_repos_java.txt \ 
 -d custom_repos/repos_dir \
 -r java_semgrep_rules \
 -s custom_repos/java_semgrep_results \
 -c custom_repos/results.csv
```

This repo also includes modified python script that adds description for manual sorting:
```console
python3 find_repos_and_add_desc.py \
    -q github_search_query \
    -f store_results_here.txt \
    -s min_size_of_repos
```

For example:
```console
python3 find_repos_and_add_desc.py \
    -q "NOT in:descritpion library NOT in:readme exercise stars:500..1000 language:Java created:>2017-01-01 sort:updated" \
    -f /home/rtz/github_vuln_research/my_semgrep_rules/java_all/java_repos_list_semgrep.txt \
    -s 20000
```



## Additonal commands
Read CSV in terminal:
```
column -s, -t < repos_report.csv | less -#2 -N -S 
```


### count the number of occurrences to remove FPs
```bash
cd /home/rtz/github_vuln_research/my_semgrep_rules/
mkdir /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go
mv go_semgrep* /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go

cd /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go
fgrep home.rtz.github_vuln_research.my_semgrep_rules. * > tmp.txt
/home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/count_words.sh tmp.txt > asd.txt 
code asd.txt
```


### generate rules from semgrep-rules repo
```bash
cd /home/rtz/github_vuln_research/semgrep-rules/go ; find `pwd` -name *.yaml  | tee /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/full_list.txt > /dev/null
python3 /home/rtz/github_vuln_research/my_semgrep_rules/remove_unwanted_rules.py /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/full_list.txt | tee /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/list.txt  > /dev/null

while read p ; do cp $p /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/; done < /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/list.txt 
rm /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/full_list.txt /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/rule_list.txt 

cd /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules
```

