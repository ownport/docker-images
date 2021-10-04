
from builder.git import RE_DEVEL_BRANCH, RE_FEATURE_BRANCH, RE_MASTER_BRANCH

GITLAB_STAGES = [ 
  'buildtools', 
  'base', 
  'python', 'python-dev', 'python-dev-vscode',
  'openjdk', 'sbt', 'scala', 
  'nodejs', 'rust', 'bigdata', 'data-science',
  'workflows', 'scraping', 'tools'
]

DOCKER_TEMPLATE_PIPELINE = '''
---
default:
  image: docker:stable

variables:
  DOCKER_TLS_CERTDIR: "/certs"

services:
- docker:stable-dind

stages:
- {STAGES}

before_script:
- docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
- apk add python3 git

buildtools:
  stage: buildtools
  script:
  - echo "[WARNING] to be added later"
'''

DOCKER_TARGET_TEMPLATE = '''
{target_name}:
  stage: {stage}
  script:
  - ./builder docker --build --target-path {target_path} --branch {branch}
  - ./builder docker --test --target-path {target_path} --branch {branch}
'''

class GitLabYAMLGenerator:

    def __init__(self, branch:str=None, tag:str=None) -> None:
        
        self._tag = tag

        if RE_DEVEL_BRANCH.match(branch):
            self._branch = 'devel'
        elif RE_MASTER_BRANCH.match(branch):
            self._branch = 'pre-release'
        elif self._tag and self._tag.startswith('release/'):
            self._branch = 'release'
        else:
            self._branch = 'test'

    def run(self, targets:list) -> None:
        ''' generate GitLab CI pipeline
        '''
        print(DOCKER_TEMPLATE_PIPELINE.format(STAGES='\n- '.join(GITLAB_STAGES)))
        for target_path in targets:
            stage, target_name = str(target_path).split("/")[-2:]
            target_name = ':'.join([stage, target_name])
            print(DOCKER_TARGET_TEMPLATE.format(target_name=target_name, 
                                                stage=stage,
                                                branch=self._branch,
                                                target_path=target_path))

            if self._branch in ('devel', 'pre-release', 'release'):
                print(f"  - ./builder docker --publish --target-path {target_path} --branch {self._branch}")
