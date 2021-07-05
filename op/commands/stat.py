from argparse import Namespace

from op.config import Config


SERVICES_PORTS = {  # TODO: deduplicate this (here and in templates/compose/*.yml)
    'db': 5432,
    'app': 8000,
    'app_second': 8001,
}


class Stat:
    def __init__(self, config: Config):
        self.config = config

    def get_name(self):
        return 'stat'

    def add_parser(self, subparsers):
        subparsers.add_parser('stat',
                              description='Show information about project.',
                              help='information about project')

    def do(self, args: Namespace):
        print('*** PORTS ***')
        print()
        for env in self.config.environments:
            print('env = {}'.format(env))
            for service, port in self.config.ports[env].items():
                print(' * {}:{} -> localhost:{}'.format(service, SERVICES_PORTS[service], port))
            print()
