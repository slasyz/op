from argparse import Namespace

from op.config import Config


class Tests:
    def __init__(self, config: Config):
        self.config = config

    def get_name(self):
        return 'tests'

    def add_parser(self, subparsers):
        parser_tests = subparsers.add_parser('tests',
                                             description='Run tests.',
                                             help='tests')

        parser_tests.add_argument('--unit', '-u',
                                   help='run only unit tests',
                                   type=bool,
                                   default=False)

    def do(self, args: Namespace):
        pass  # TODO: run integration tests in Docker or unit tests on host machine
