
from builder.git import RE_MASTER_BRANCH
from builder.git import RE_DEVEL_BRANCH
from builder.git import RE_BUGFIX_BRANCH
from builder.git import RE_FEATURE_BRANCH
from builder.git import RE_EXTRACT_BRANCH_AND_NUM


def get_tag_suffix(branch:str, tag:str) -> str:
    ''' return a tag suffix based on branch and tag name
    '''
    tag_suffix = '-'
    if RE_DEVEL_BRANCH.match(branch):
        tag_suffix += 'devel'
    elif RE_MASTER_BRANCH.match(branch):
        tag_suffix += 'pre-release'
    elif RE_FEATURE_BRANCH.match(branch) or RE_BUGFIX_BRANCH.match(branch):
        tag_suffix += '-'.join(RE_EXTRACT_BRANCH_AND_NUM.search(branch).groups())
    elif tag and tag.startswith('release/'):
        tag_suffix = ''

    return tag_suffix
