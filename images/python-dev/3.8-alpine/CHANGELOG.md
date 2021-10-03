# CHANGELOG

## 3.8-dev-alpine

Build dependencies
- gcc python3-dev musl-dev libffi-dev

Tools
- git jq zsh make zip
- py3-wheel py3-setuptools

Build and deploy tools
- twine build
- setuptools_scm[toml]>=3.4

Python Tools
- pip-tools

Git Tools
- pre-commit

Linters
- pylint

Testing
- pytest pytest-cov pytest-xdist 
- pytest-benchmark pytest-mock
- coverage[toml]
