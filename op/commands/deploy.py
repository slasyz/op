from argparse import Namespace

from op.config import Config
from op.docker import Docker


class Deploy:
    def __init__(self, config: Config, deployer: Docker):
        self.config = config
        self.deployer = deployer

    def get_name(self):
        return 'deploy'

    def add_parser(self, subparsers):
        parser_deploy = subparsers.add_parser('deploy',
                                              description='Deploy project to the environment.',
                                              help='deploy project to the environment')

        parser_deploy.add_argument('--env', '-e',
                                   type=str,
                                   choices=self.config.environments)

    def do(self, args: Namespace):
        self.deployer.assure()
        self.deployer.deploy(args.env)
