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
cd ~
mkdir go_semgrep_rules
git clone https://github.com/returntocorp/semgrep-rules.git

cd ~/semgrep-rules/go ; find `pwd` -name *.yaml  | tee ~/go_semgrep_rules/full_list.txt > /dev/null

python3 remove_unwanted_rules.py ~/go_semgrep_rules/full_list.txt | tee ~/go_semgrep_rules/list.txt > /dev/null

while read p ; do cp $p ~/go_semgrep_rules/; done < ~/go_semgrep_rules/list.txt

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
- clone the repository from list,
- run semgrep using given config (directory with rules),
- store reports in given directory,
- store results in csv format in specified path.

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
`-c/--csv` - semgrep results in csv format

For example:
```console
python3 generateReport.py -l ~/java_repos.txt \ 
 -d ~/java_tmp_repo \
 -r ~/java_semgrep_rules \
 -s ~/java_semgrep_results \
 -c ~/results.csv
```
```console
rtz@debian:~/Java_repos_all_example$ ls -la 
total 116
drwxr-xr-x  2 rtz rtz  4096 Feb  5 05:42 .
drwxr-xr-x 24 rtz rtz  4096 Apr 25 12:29 ..
-rw-r--r--  1 rtz rtz   170 Feb  5 05:33 java_repos.txt
-rw-r--r--  1 rtz rtz  5956 Feb  5 05:42 java_semgrep_results_someRepoOne.txt
-rw-r--r--  1 rtz rtz 26685 Feb  5 05:42 java_semgrep_results_someRepoTwo.txt
-rw-r--r--  1 rtz rtz 44561 Feb  5 05:42 java_semgrep_results_someRepoThree.txt
-rw-r--r--  1 rtz rtz   247 Feb  5 05:41 results.csv
```

## Other stuff

This repo also includes modified find_repos.py that adds description for manual sorting:
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

`makeAll.py` clones semgrep rules repository and copies security rules to given directory.

### Read CSV in terminal:
```
column -s, -t < repos_report.csv | less -#2 -N -S 
```


### Count the number of occurrences to remove FPs
```bash
cd /home/rtz/github_vuln_research/my_semgrep_rules/
mkdir /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go
mv go_semgrep* /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go

cd /home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/go
fgrep home.rtz.github_vuln_research.my_semgrep_rules. * > tmp.txt
/home/rtz/github_vuln_research/my_semgrep_rules/custom_repos/count_words.sh tmp.txt > pmt.txt 
code pmt.txt
```