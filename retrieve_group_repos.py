import os

import gitlab

gitlab_server = os.getenv('gitlab_server_addr')
gitlab_token = os.getenv('gitlab_token')
gitlab_group_name = 'eis'

gl = gitlab.Gitlab(gitlab_server, private_token=gitlab_token, ssl_verify=False)

group = gl.groups.get(gitlab_group_name)
projects = group.projects.list(all=True)
for project in projects:
    print(project.name, project)