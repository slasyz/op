from argparse import Namespace

from op.config import Config


class Logs:
    def __init__(self, config: Config):
        self.config = config

    def get_name(self):
        return 'help'

    def add_parser(self, subparsers):
        parser = subparsers.add_parser('help',
                                       description='Attach to logs.',
                                       help='attach to logs')

        parser.add_argument('--env', '-e',
                            type=str,
                            choices=self.config.environments)

    def do(self, args: Namespace):
        pass  # TODO: attach and show logs
