
import logging

from builder.git import RE_MASTER_BRANCH
from builder.git import RE_DEVEL_BRANCH
from builder.git import RE_BUGFIX_BRANCH
from builder.git import RE_FEATURE_BRANCH
from builder.git import RE_EXTRACT_BRANCH_AND_NUM

logger = logging.getLogger(__name__)


TEMPLATE_PIPELINE = '''
---
default:
  # image: docker:stable
  image: registry.gitlab.com/ownport/docker-images/release/kaniko-builder:1.6-ubuntu

# variables:
#   DOCKER_TLS_CERTDIR: "/certs"

# services:
# - docker:stable-dind

stages:
- {STAGES}

# before_script:
# - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
# - apk add python3 git

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
  - ./builder docker --publish --target-path {target_path} --branch {branch}
'''

KANIKO_TARGET_TEMPLATE = '''
{target_name}:
  stage: {stage}
  script:
  - ./builder kaniko --build --target-path {target_path} --branch {branch}
'''

class GitLabYAMLGenerator:

    def __init__(self, branch:str=None, tag:str=None, settings:dict={}) -> None:
        
        self._tag = tag
        self._settings = settings

        if RE_DEVEL_BRANCH.match(branch):
            self._branch = 'devel'
        elif RE_MASTER_BRANCH.match(branch):
            self._branch = 'pre-release'
        elif self._tag and self._tag.startswith('release/'):
            self._branch = 'release'
        elif RE_FEATURE_BRANCH.match(branch) or RE_BUGFIX_BRANCH.match(branch):
            self._branch = '-'.join(RE_EXTRACT_BRANCH_AND_NUM.search(branch).groups())

    def run(self, targets:list) -> None:
        ''' generate GitLab CI pipeline
        '''
        print(TEMPLATE_PIPELINE.format(
                        STAGES='\n- '.join(
                                        self._settings.get('stages', [])
                        )
        ))
        for target_path in targets:
            try:
                stage, target_name = str(target_path).split("/")[-2:]
                target_name = ':'.join([stage, target_name])
                print(KANIKO_TARGET_TEMPLATE.format(target_name=target_name, 
                                                    stage=stage,
                                                    branch=self._branch,
                                                    target_path=target_path))
            except:
                logger.warning(f'Cannot detect stage and target name from target path, ${target_path}')
