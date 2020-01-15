import os
from pathlib import Path

import gitlab
from git import Repo

gitlab_server = os.getenv('gitlab_server_addr')
gitlab_token = os.getenv('gitlab_token')
gitlab_group_names = ['eis']

repo_root_dir = os.path.join(str(Path.home()), 'downloads', 'repos')

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
            Repo.clone_from(project.http_url_to_repo, os.path.join(destination, clone_path))
