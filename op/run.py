import subprocess
import sys
from typing import Sequence, Optional


def run_commands(commands: Sequence[Optional[str]], env_vars: dict = None):
    for command in commands:
        if command is None:
            continue
        run_command(command, env_vars)


def run_command(command: str, env_vars: dict = None):
    print(f'$ {command}')
    subprocess.run(command, env=env_vars, check=True, shell=True, stdout=sys.stdout, stderr=sys.stderr)


def get_output(command: str, env_vars: dict = None) -> str:
    print(f'$ {command}')
    result = subprocess.run(command, env=env_vars, check=True, shell=True, capture_output=True)

    stdout = result.stdout.decode('utf-8')
    if stdout:
        print(stdout, end='')
    stderr = result.stderr.decode('utf-8')
    if stderr:
        print(stderr, end='')

    return result.stdout.decode('utf-8').strip()
