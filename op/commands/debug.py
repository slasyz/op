from argparse import Namespace


class Debug:
    def get_name(self):
        return 'debug'

    def add_parser(self, subparsers):
        subparsers.add_parser('debug',
                              description='Start project dependencies so it could be run on host machine',
                              help='start project dependencies')

    def do(self, args: Namespace):
        pass  # TODO: start dependencies in Docker
