import os

import gitlab

gitlab_server = os.getenv('gitlab_server_addr')
gitlab_token = os.getenv('gitlab_token')

gl = gitlab.Gitlab(gitlab_server, private_token=gitlab_token, ssl_verify=False)

gl.auth()

print(f"Projects owned by user {gl.user.name}")

projects = gl.projects.list(owned=True)
for project in projects:
    print(project.name, project)

