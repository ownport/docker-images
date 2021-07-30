
from buildtools.git import RE_DEVEL_BRANCH, RE_MASTER_BRANCH

DOCKER_TEMPLATE_PIPELINE = '''
---
default:
  image: docker:stable

variables:
  DOCKER_TLS_CERTDIR: "/certs"

services:
- docker:stable-dind

stages:
- buildtools
- base
- python

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
  - python3 -m buildtools docker --build --target-path {target_path} {dev_image}
  - python3 -m buildtools docker --test --target-path {target_path} {dev_image}
'''

class GitLabYAMLGenerator:

    def __init__(self, branch: str) -> None:
        
        self._branch = branch
        self._dev_image = "--dev-image" if RE_DEVEL_BRANCH.match(self._branch) else ""

    def run(self, targets:list) -> None:
        ''' generate GitLab CI pipeline
        '''
        print(DOCKER_TEMPLATE_PIPELINE)
        for target_path in targets:
            stage, target_name = str(target_path).split("/")[-2:]
            target_name = ':'.join([stage, target_name])
            print(DOCKER_TARGET_TEMPLATE.format(target_name=target_name, 
                                                stage=stage,
                                                dev_image=self._dev_image,
                                                target_path=target_path))

            if RE_MASTER_BRANCH.match(self._branch) or RE_DEVEL_BRANCH.match(self._branch):
                print(f"  - python3 -m buildtools docker --publish --target-path {target_path} {self._dev_image}")