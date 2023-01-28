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


```console
cd /home/rtz/github_vuln_research/semgrep-rules/ruby ; find `pwd` -name *.yaml  | tee /home/rtz/github_vuln_research/my_semgrep_rules/ruby/full_list.txt > /dev/null
python3 /home/rtz/github_vuln_research/my_semgrep_rules/remove_unwanted_rules.py /home/rtz/github_vuln_research/my_semgrep_rules/ruby/full_list.txt | tee /home/rtz/github_vuln_research/my_semgrep_rules/ruby/rule_list.txt 
while read p ; do cp $p /home/rtz/github_vuln_research/my_semgrep_rules/ruby/; done < /home/rtz/github_vuln_research/my_semgrep_rules/ruby/rule_list.txt 
rm /home/rtz/github_vuln_research/my_semgrep_rules/ruby/full_list.txt /home/rtz/github_vuln_research/my_semgrep_rules/ruby/rule_list.txt 
cd /home/rtz/github_vuln_research/my_semgrep_rules/ruby
```

python3 /home/rtz/github_vuln_research/repo-finding-tool/find_repos.py -q "stars:500..10000 language:Java  created:>2017-01-01 sort:updated" -f /home/rtz/github_vuln_research/my_semgrep_rules/java_repo_list.txt -s 10000

python3 /home/rtz/github_vuln_research/repo-finding-tool/find_repos.py -q "stars:500..10000 language:PHP  created:>2017-01-01 sort:updated" -f /home/rtz/github_vuln_research/my_semgrep_rules/php_repo_list.txt -s 10000

python3 /home/rtz/github_vuln_research/repo-finding-tool/find_repos.py -q "stars:500..10000 language:Ruby  created:>2017-01-01 sort:updated" -f /home/rtz/github_vuln_research/my_semgrep_rules/ruby_repo_list.txt -s 10000

python3 /home/rtz/github_vuln_research/repo-finding-tool/find_repos.py -q "stars:500..10000 language:Go  created:>2017-01-01 sort:updated" -f /home/rtz/github_vuln_research/my_semgrep_rules/go_repo_list.txt -s 10000

python3 /home/rtz/github_vuln_research/repo-finding-tool/find_repos.py -q "stars:500..10000 language:C#  created:>2017-01-01 sort:updated" -f /home/rtz/github_vuln_research/my_semgrep_rules/csharp_repo_list.txt -s 10000

python3 /home/rtz/github_vuln_research/repo-finding-tool/find_repos.py -q "stars:500..5000 language:Python  created:>2017-01-01 sort:updated" -f /home/rtz/github_vuln_research/my_semgrep_rules/python_repo_list.txt -s 20000



curl \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/code?q=Q&per_page=100"

python3 /home/rtz/github_vuln_research/repo-finding-tool/find_repos.py -q "stars:500..10000 language:Java  created:>2017-01-01 sort:updated" -f /home/rtz/github_vuln_research/my_semgrep_rules/java_repo_list.txt
python3 /home/rtz/github_vuln_research/repo-finding-tool/find_repos.py -q "stars:500..10000 language:PHP  created:>2017-01-01 sort:updated" -f /home/rtz/github_vuln_research/my_semgrep_rules/php_repo_list.txt


stars:500..10000 language:Go  created:>2017-01-01 sort:updated

curl \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/repositories?q=repo:returntocorp/semgrep"



```python
 
```







# Unrelevant

```bash
#cat /home/rtz/github_vuln_research/repoList.txt | awk -F "/" '{print $4}' > repo_names.txt

cd /home/rtz/github_vuln_research/repos
rm -rf /home/rtz/github_vuln_research/repos/*
rm -rf /home/rtz/github_vuln_research/semgrep_results/*

while read p; do 
    a=$(echo $p |awk -F "/" '{print $5}'); git clone $p.git;python3 -m semgrep --config=auto $a  | tee /home/rtz/github_vuln_research/semgrep_results/$a.txt ; python3 -m semgrep --config "p/r2c-security-audit" $a | tee -a /home/rtz/github_vuln_research/semgrep_results/$a.txt ; rm -rf $a ; sleep 90
done < /home/rtz/github_vuln_research/repoList.txt
```

## commnads
Add .git at the end of each url
```bash
awk '{print $0".git"}' repoList.txt > newRepoList.txt
# OR vim
# :%norm A*
# :%s/$/\*/g
```
Get size of each repo
curl https://api.github.com/repos/dotnet/roslyn --header "Authorization: Bearer Personal_Token" 2>/dev/null | grep size | tr -dc '[:digit:]'
```bash
while read p; do
    curl --url $p --header "Authorization: Bearer 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" 2>/dev/null | grep size | tr -dc '[:digit:]';echo; sleep 5
done < reposGetSize.txt
```

auto is default rule set
python3 -m semgrep --config=auto wondercms
python3 -m semgrep --config "p/r2c-security-audit" wondercms

