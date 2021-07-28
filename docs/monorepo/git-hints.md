# Git Hints

The command finds the most recent tag that is reachable from a commit.
If the tag points to the commit, then only the tag is shown.
Otherwise, it suffixes the tag name with the number of additional commits on top of the tagged object and the abbreviated object name of the most recent commit.
```sh
git describe
```

With `--abbrev` set to 0, the command can be used to find the closest tagname without any suffix:
```sh
git describe --abbrev=0
```
To get tag from current branch
```sh
git describe --abbrev=0 --tags
``` 
To get tags across all branches, not just the current branch
```sh
git describe --tags `git rev-list --tags --max-count=1`
```

To get the most recent tag, you can do:
```sh
git for-each-ref refs/tags --sort=-taggerdate --format='%(refname)' --count=1
```
To get last 2 tags
```sh
git for-each-ref refs/tags --sort=-taggerdate --format='%(refname)' --count=2
```
or 
```sh
git for-each-ref refs/tags --sort=-taggerdate --format=%\(tag\) --count=2
```

