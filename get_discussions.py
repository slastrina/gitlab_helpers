import json
import os
from collections import defaultdict
from datetime import date
import gitlab

gitlab_server = os.getenv('gitlab_server_addr')
gitlab_token = os.getenv('gitlab_token')

gl = gitlab.Gitlab(gitlab_server, private_token=gitlab_token, ssl_verify=False)

gl.auth()

projects = [
    'pni/spatialnet',
    'pni/spatialstorm',
    'pni/devops',
    'pni/ods'
]

target_types = [
    'DiffNote',
    'Note'
]

stats = defaultdict(lambda: {'Note': 0, 'DiffNote': 0})

page_limit = 20
current_date = date.today().strftime("%Y-%m-%d")
print(current_date)

for project in projects:
    obj = gl.projects.get(project)
    for page in range(page_limit):
        events = obj.events.list(action='commented', page=page, per_page=100, after='2020-01-01', before=current_date, sort='desc')
        for x in events:
            if x.author['name'] != 'svc_pni_prd_jenkins' and x.target_type in target_types:
                print(project, x, x.action_name, x.target_type, x.author['name'])
                stats[x.author['name']][x.target_type] += 1

print(json.dumps(stats, indent=4, sort_keys=True))
