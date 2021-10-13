
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
  image: registry.gitlab.com/ownport/docker-images/release/kaniko:1.6-slim

# variables:
#   DOCKER_TLS_CERTDIR: "/certs"

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

KANIKO_TARGET_TEMPLATE = '''
{target_name}:
  stage: {stage}
  script:
  - mkdir -p /kaniko/.docker/ && \
    /kaniko/update-docker-config.sh && \
    /kaniko/executor \
      --context /builds/ownport/docker-images/{target_path} \
      --build-arg BRANCH={branch} \
      --cache \
      --destination {image_uri} 
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
        for target in targets:
            try:
                target_name = ':'.join([
                                    target.info.get('stage'), 
                                    target.info.get('target_name')])
                print(
                  KANIKO_TARGET_TEMPLATE.format(target_name=target_name, 
                                                stage=target.info.get('stage'),
                                                branch=self._branch,
                                                target_path=target.path,
                                                image_uri=target.image_uri))
            except:
                logger.warning(f'Cannot detect stage and target name from target path, {target.path}')
