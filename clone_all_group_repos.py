import os
from pathlib import Path

import gitlab
from git import Repo

gitlab_server = os.getenv('gitlab_server_addr')
gitlab_token = os.getenv('gitlab_token')
gitlab_group_name = 'eis'

destination = os.path.join(str(Path.home()), 'downloads/repos/')

os.makedirs(destination, exist_ok=True)

gl = gitlab.Gitlab(gitlab_server, private_token=gitlab_token, ssl_verify=False)

group = gl.groups.get(gitlab_group_name)
projects = group.projects.list(all=True)
for project in projects:
    print('Cloning:', project.name, project.http_url_to_repo)
    Repo.clone_from(project.http_url_to_repo, os.path.join(destination, project.name))
