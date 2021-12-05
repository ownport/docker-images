# GilLab Container Registry

## How to get list active features

```sh
curl --header "PRIVATE-TOKEN: <TOKEN>" https://gitlab.com/api/v4/projects/<PROJECT_ID> | jq .
```

## How to set feature flag

```sh
curl --request PUT https://gitlab.com/api/v4/projects/23580555 \
     --header "PRIVATE-TOKEN: Jr6FYshkq_8Ms2imMqSB" \
     --header 'Accept: application/json' \
     --header 'Content-Type: application/json' \
     --data-raw '{ "ci_job_token_scope_enabled": true}'
```

{"error":"allow_merge_on_skipped_pipeline, autoclose_referenced_issues, auto_devops_enabled, auto_devops_deploy_strategy, auto_cancel_pending_pipelines, build_coverage_regex, build_git_strategy, build_timeout, builds_access_level, ci_config_path, ci_default_git_depth, ci_forward_deployment_enabled, container_registry_access_level, container_expiration_policy_attributes, default_branch, description, emails_disabled, forking_access_level, issues_access_level, lfs_enabled, merge_pipelines_enabled, merge_requests_access_level, merge_requests_template, merge_trains_enabled, merge_method, name, only_allow_merge_if_all_discussions_are_resolved, only_allow_merge_if_pipeline_succeeds, pages_access_level, path, printing_merge_request_link_enabled, public_builds, remove_source_branch_after_merge, repository_access_level, request_access_enabled, resolve_outdated_diff_discussions, restrict_user_defined_variables, squash_option, shared_runners_enabled, snippets_access_level, tag_list, topics, visibility, wiki_access_level, avatar, suggestion_commit_message, repository_storage, compliance_framework_setting, packages_enabled, service_desk_enabled, keep_latest_artifact, issues_enabled, jobs_enabled, merge_requests_enabled, wiki_enabled, snippets_enabled, container_registry_enabled, approvals_before_merge, external_authorization_classification_label, fallback_approvals_required, import_url, issues_template, merge_requests_template, merge_pipelines_enabled, merge_trains_enabled are missing, at least one parameter must be provided"}