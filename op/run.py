import subprocess
import sys
from typing import Sequence


def run(commands: Sequence[Sequence[str]], env_vars: dict):
    for cmd in commands:
        rc = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, env=env_vars)
        if rc != 0:
            sys.exit(rc)
