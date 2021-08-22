import os
from argparse import Namespace


class Init:
    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir

    def get_name(self):
        return 'init'

    def add_parser(self, subparsers):
        subparsers.add_parser('init',
                              description='Initialize op-based project.',
                              help='initialize project')

    def do(self, args: Namespace):
        with open(os.path.join(self.templates_dir, 'op.toml'), encoding='utf-8') as f:
            content = f.read()

        with open('op.toml', 'x', encoding='utf-8') as f:
            f.write(content)
