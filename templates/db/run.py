# TODO: replace run.py with shell script using `jq` or `yq` for json or yaml parsing
#  or with golang script and use it from scratch.

{% if config == 'json' %}import json{% elif config == 'yaml' %}import yaml{% endif %}
import os
import subprocess
import sys

print('database: loading config (stdout)', file=sys.stdout)
print('database: loading config (stderr)', file=sys.stderr)

{% if config == 'json' %}with open('/etc/{{ short_name }}/config.json') as f:
    data = json.load(f)
{% elif config == 'yaml' %}with open('/etc/{{ short_name }}/config.yml') as f:
    data = yaml.load(f)
{% endif %}

env = dict(os.environ)  # Make a copy of the current environment
env['POSTGRES_DB'] = data['database']['name']
env['POSTGRES_USER'] = data['database']['user']
env['POSTGRES_PASSWORD'] = data['database']['pass']

print("env:", env)

code = subprocess.call(['docker-entrypoint.sh', 'postgres'], env=env)
if code != 0:
    exit(code)
