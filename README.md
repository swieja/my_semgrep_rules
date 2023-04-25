# Project notes
A set of scripts and stuff to utilize [repo-find](https://github.com/jkob-sec/repo-find) and semgrep stolen from [semgrep-rules](https://github.com/returntocorp/semgrep-rules) for vulnerability research in  open source projects on github. 

This requires [semgrep CLI](https://semgrep.dev/docs/getting-started/) to be installed:

stolen semgrep rules mostly include:
- classic rce attack (command injection)
- deseralization
- lfi
- ssrf
- sqli

source: \
https://github.com/returntocorp/semgrep-rules \
https://semgrep.dev/explore
## How to use
1. Generate list of repos using [repo-find](https://github.com/jkob-sec/repo-find) or use an existing list.

```console
python3 find_repos.py -q "stars:500..1000 language:Java created:>2017-10-11 sort:updated" -f ~/repo_list_java.txt -s 10000 -d
```

2. Clone [semgrep-rules](https://github.com/returntocorp/semgrep-rules), copy .yaml rules to desired directory and remove unwanted rules (low/medium severity).

remove_unwanted_rules.py
```python
[...]
if not any (string in file_contents.lower() for string in ["xss","csrf","redirect","category: correctness","category: best-practice","this rule has been deprecated","improper encoding or escaping of output"]):
```

```console
cd ~/semgrep-rules/go ; find `pwd` -name *.yaml  | tee ~/go_semgrep_rules/full_list.txt > /dev/null

python3 /home/rtz/github_vuln_research/my_semgrep_rules/remove_unwanted_rules.py ~/go_semgrep_rules/full_list.txt | tee ~/go_semgrep_rules/list.txt > /dev/null

while read p ; do cp $p ~/go_semgrep_rules/; done < /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/list.txt

rtz@debian:~/go_semgrep_rules$ ls -la 
total 156
drwxr-xr-x  2 rtz rtz 4096 Apr  6 04:24 .
drwxr-xr-x 24 rtz rtz 4096 Apr 14 05:57 ..
-rw-r--r--  1 rtz rtz  642 Apr  6 04:24 bad_tmp.yaml
-rw-r--r--  1 rtz rtz 1025 Apr  6 04:24 bind_all.yaml
-rw-r--r--  1 rtz rtz 1044 Apr  6 04:24 cookie-missing-secure.yaml
-rw-r--r--  1 rtz rtz 1238 Apr  6 04:24 dangerous-command-write.yaml
-rw-r--r--  1 rtz rtz 2439 Apr  6 04:24 dangerous-exec-cmd.yaml
[...]
```

3. Run generateReport.py, it will:
- clone the repository,
- run semgrep using given config (directory with rules)
- store reports in given directory
- store results in csv format in specified path

```console
python3 generateReport.py -l ~/repo_list \
 -d ~/tmp_repo_dir \
 -r ~/semgrep_rules_dir \
 -s ~/semgrep_results_dir \
 -c ~/semgrep_results_csv
```
`-l/--list` - file with a list of repositories \
`-d/--directory` - temporary directory where repository will be cloned \
`-r/--rules` - directory with semgrep rules  \
`-s/--save` - directory where semgrep results for each repo will be stored \
`-c/--csv` - semgrep results in csv format  \

For example:
```console
python3 generateReport.py -l ~/java_repos.txt \ 
 -d ~/java_tmp_repo \
 -r ~/java_semgrep_rules \
 -s ~/java_semgrep_results \
 -c ~/results.csv
```

tba


## Other scripts

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
    -f repo_list_java.txt \
    -s 20000
```

`remove_unwanted_rules.py` removes rules that detect low and mid severity vulnerabilities such as xss, csrf, tls attacks etc.

`makeAll.py` clones semgrep rules repository and copies security rules to given directory.

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
/home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/count_words.sh tmp.txt > pmt.txt 
code pmt.txt
```


### generate rules from semgrep-rules repo
```bash
cd /home/rtz/github_vuln_research/semgrep-rules/go ; find `pwd` -name *.yaml  | tee /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/full_list.txt > /dev/null
python3 /home/rtz/github_vuln_research/my_semgrep_rules/remove_unwanted_rules.py /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/full_list.txt | tee /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/list.txt  > /dev/null

while read p ; do cp $p /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/; done < /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/list.txt 
rm /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/full_list.txt /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules/rule_list.txt 

cd /home/rtz/github_vuln_research/my_semgrep_rules/go_semgrep_rules
```

