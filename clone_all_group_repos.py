"""
Usage:
* Create environment variables:
  * gitlab_server_addr (your gitlab server address i.e. https://gitlab.com)
  * gitlab_token (your gitlab access token)

* Set list of groups in the variable: gitlab_group_names
* Set clone root directory in the variable: repo_root_dir

Output directory will be /repo_root/gitlab_group_name/gitlab_repo_name/

If the directory exists, this tool will instead perform a fetch on all remotes for the given repo
"""

import os
from pathlib import Path

import gitlab
from git import Repo, GitCommandError

gitlab_server = os.getenv('gitlab_server_addr')
gitlab_token = os.getenv('gitlab_token')

gitlab_group_names = [
    'eis',
    'pni',
    'elms',
    'fls',
]

repo_root_dir = os.path.join(str(Path.home()), 'git', 'nbnco')

gl = gitlab.Gitlab(gitlab_server, private_token=gitlab_token, ssl_verify=False)

for group_name in gitlab_group_names:
    destination = os.path.join(repo_root_dir, group_name)
    os.makedirs(destination, exist_ok=True)

    print(f"Retrieving list of {group_name} repository's")
    group = gl.groups.get(group_name)
    projects = group.projects.list(all=True)

    for project in projects:
        clone_path = os.path.join(destination, project.name)

        if os.path.exists(clone_path):
            for remote in Repo(clone_path).remotes:
                print(f'Fetching {group_name}:', project.name, remote.name)
                remote.fetch()
        else:
            print(f'Cloning {group_name}:', project.name, project.http_url_to_repo)
            try:
                Repo.clone_from(project.http_url_to_repo, os.path.join(destination, clone_path))
            except GitCommandError as ex:
                print(f'Probably dont have permission to download: {ex}')
            except Exception as ex:
                print(ex)