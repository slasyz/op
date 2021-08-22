from argparse import Namespace

from op.config import Config
from op.docker import Docker


class Tests:
    def __init__(self, config: Config, deployer: Docker):
        self.config = config
        self.deployer = deployer

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
        if args.unit:
            if self.config.language == 'python':
                pass
                # export PYTHON_INTERPRETER = $(shell ( ls ./venv/Scripts/python.exe ./venv/bin/python 2> /dev/null || echo python ) | head -n 1)
                # $(PYTHON_INTERPRETER) -m pytest tests/unit
            else:
                pass  # TODO: run unit tests on host machine
        else:
            self.deployer.assure('tests')
            self.deployer.integration_tests()
