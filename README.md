# Project notes
semgrep command to run all rules from `java` directory to scan vespa source code
python3 -m semgrep --config /home/rtz/github_vuln_research/my_semgrep_rules/java /home/rtz/github_vuln_research/vespa


classic rce \
seralization \
lfi \
ssrf \












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

