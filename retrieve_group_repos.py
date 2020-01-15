import gitlab
import os

gitlab_server = os.getenv('gitlab_server_addr')
gitlab_token = os.getenv('gitlab_token')
destination = None

gl = gitlab.Gitlab(gitlab_server, private_token=gitlab_token, ssl_verify=False)

group = gl.groups.get('eis')
projects = group.projects.list(all=True)
for project in projects:
    print(project.http_url_to_repo)

