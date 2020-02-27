import os

import gitlab

gitlab_server = os.getenv('gitlab_server_addr')
gitlab_token = os.getenv('gitlab_token')

gl = gitlab.Gitlab(gitlab_server, private_token=gitlab_token, ssl_verify=False)

gl.auth()

print(f"Projects owned by user {gl.user.name}")

mrs = gl.mergerequests.list()
for mr in mrs:
    print(mr)

