# GitLab variables in different phases

| Variable                        | Commit/push to feature branch                                | Merge request to devel branch | Merge request to master branch | tagging in master branch |                    |
| ------------------------------- | ------------------------------------------------------------ | ----------------------------- | ------------------------------ | ------------------------ | ------------------ |
| CI_COMMIT_BRANCH                | feature/24-research-for-gitlab-ci-predefined-variables-for-different-situations | devel                         | master                         |                          |                    |
| CI_COMMIT_REF_NAME              | feature/24-research-for-gitlab-ci-predefined-variables-for-different-situations | devel                         | master                         | release/20210728.2       | release/20210728.3 |
| CI_COMMIT_REF_SLUG              | feature-24-research-for-gitlab-ci-predefined-variables-for-diff | devel                         | master                         | release-20210728-2       | release/20210728.3 |
| CI_COMMIT_TAG                   |                                                              |                               |                                | release/20210728.2       | release/20210728.3 |
| CI_DEFAULT_BRANCH               | devel                                                        | devel                         | devel                          | devel                    | devel              |
| CI_PIPELINE_SOURCE              | push                                                         | push                          | push                           | push                     | push               |
| git rev-parse --abbrev-ref HEAD | HEAD                                                         | HEAD                          | HEAD                           | HEAD                     | HEAD               |

