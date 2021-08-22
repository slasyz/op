from argparse import Namespace

from op.config import Config
from op.run import get_output, run_commands


class Logs:
    def __init__(self, config: Config):
        self.config = config

    def get_name(self):
        return 'logs'

    def add_parser(self, subparsers):
        parser = subparsers.add_parser('logs',
                                       description='Attach to logs.',
                                       help='attach to logs')

        parser.add_argument('--env', '-e',
                            type=str, required=True,
                            choices=self.config.environments)
        parser.add_argument('service', metavar='SERVICE', type=str,
                            choices=self.config.services,
                            help='service to check logs')

    def do(self, args: Namespace):
        container = get_output('docker --context {short_name}_{env} ps -f name={short_name}_{env}_{service} --quiet'.format(
            short_name=self.config.short_name,
            env=args.env,
            service=args.service,
        ))

        run_commands(['docker --context {short_name}_{env} logs --tail 50 --follow --timestamps {container}'.format(
            short_name=self.config.short_name,
            env=args.env,
            container=container,
        )])
