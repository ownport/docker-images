# Monorepo Hints

## Git

**Are there any differences from HEAD?**
```sh
git diff-index --quiet HEAD
```
If the exit code is 0, then there were no differences.

**What files have changed from HEAD?**
```sh
git diff-index --name-only HEAD
```

**What files have changed from HEAD, and in what ways have they changed (added, deleted, changed)?**
```sh
git diff-index --name-status HEAD
```
Add -M (and -C) if you want rename (and copy) detection.

These commands will check both the staged contents (what is in the index) and the files in the working tree. Alternatives like `git ls-files -m` will only check the working tree against the index (i.e. they will disregard any staged (but uncommitted) content that is also in the working tree).

## References

- How to optimize your CI/CD for Monorepo Node projects with Gitlab CI? https://www.padok.fr/en/blog/ci-cd-monorepo-node-gitlab
- https://stackoverflow.com/questions/3882838/whats-an-easy-way-to-detect-modified-files-in-a-git-workspace

