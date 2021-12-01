
import logging


from builder.git import RE_MASTER_BRANCH
from builder.git import RE_DEVEL_BRANCH
from builder.git import RE_BUGFIX_BRANCH
from builder.git import RE_FEATURE_BRANCH
from builder.git import RE_EXTRACT_BRANCH_AND_NUM

from jinja2 import Environment, BaseLoader, select_autoescape

logger = logging.getLogger(__name__)


TEMPLATE_PIPELINE = '''
---
stages:
- {STAGES}

buildtools:
  stage: buildtools
  script:
  - echo "[WARNING] to be added later"
'''

KANIKO_TARGET_TEMPLATE = '''
{{ target_name }}:
  stage: {{ stage }}
  image:
    name: registry.gitlab.com/ownport/docker-images/kaniko:1.7-slim
    entrypoint: [""]
  script:
  - /kaniko/update-docker-config.sh && \
    /kaniko/executor \
        --context /builds/ownport/docker-images/{{ target_path }} \
        --build-arg TAG_SUFFIX={{ tag_suffix }} \
        --destination {{ image_uri }}
'''

#   - mkdir -p /kaniko/.docker/ && \
#     /kaniko/update-docker-config.sh && \
#     /kaniko/executor \
#       --context /builds/ownport/docker-images/{target_path} \
#       --build-arg BRANCH={branch} \
#       --destination {image_uri} 

#   image:
#     name: gcr.io/kaniko-project/executor:debug
#     entrypoint: [""]
#   script:
#   - mkdir -p /kaniko/.docker
#   - echo "{\\\"auths\\\":{\\\"${CI_REGISTRY}\\\":{\\\"auth\\\":\\\"$(printf "%s:%s" "${CI_REGISTRY_USER}" "${CI_REGISTRY_PASSWORD}" | base64 | tr -d '\\n')\\\"}}}" > /kaniko/.docker/config.json
#   - /kaniko/executor \
#     --context /builds/ownport/docker-images/{{ target_path }} \
#     --dockerfile /builds/ownport/docker-images/{{ target_path }}/Dockerfile \
#     --build-arg TAG_SUFFIX={{ tag_suffix }} \
#     --destination {{ image_uri }}


class GitLabYAMLGenerator:

    def __init__(self, branch:str=None, tag:str=None, settings:dict={}) -> None:
        
        self._tag = tag
        self._settings = settings

        self._tag_suffix = '-'
        if RE_DEVEL_BRANCH.match(branch):
            self._tag_suffix += 'devel'
        elif RE_MASTER_BRANCH.match(branch):
            self._tag_suffix += 'pre-release'
        elif RE_FEATURE_BRANCH.match(branch) or RE_BUGFIX_BRANCH.match(branch):
            self._tag_suffix += '-'.join(RE_EXTRACT_BRANCH_AND_NUM.search(branch).groups())
        elif self._tag and self._tag.startswith('release/'):
            self._tag_suffix = ''


    def get_image_uri(self, registry:str, image_name:str, version:str) -> str:
        ''' returns image uri based on registry, image name and version
        '''
        if not registry:
            logger.error(f'Missed registry parameter, registry: {registry}')
            return None
        
        if not image_name:
            logger.error(f'Missed image name parameters, image_name: {image_name}')
            return None

        image_uri = "/".join([registry, image_name])
        image_version = ''.join([version, self._tag_suffix])

        return ":".join([image_uri, image_version])

    def run(self, targets:list) -> None:
        ''' generate GitLab CI pipeline
        '''
        registry = self._settings.get('registry', None)
        if not registry:
            logger.error('Missed regsitry parameter in builder gitlab configuration')
            return

        kaniko_template = Environment(
                            loader=BaseLoader(), autoescape=select_autoescape()
                        ).from_string(KANIKO_TARGET_TEMPLATE)


        print(TEMPLATE_PIPELINE.format(
                        STAGES='\n- '.join(
                                        self._settings.get('stages', [])
                        )
        ))
        for target in targets:
            
            # skip target if no definiton in settings file
            if not target.info.get('stage') in self._settings.get('stages', []):
                continue

            target_name = ':'.join([
                                target.info.get('stage'), 
                                target.info.get('target_name')])
            image_uri = self.get_image_uri(registry, target.name, target.version)
 

            print(
                kaniko_template.render(target_name=target_name, 
                                        stage=target.info.get('stage'),
                                        tag_suffix=self._tag_suffix,
                                        target_path=target.path,
                                        image_uri=image_uri))
