from argparse import Namespace

from op.config import Config
from op.run import run_commands


class Debug:
    def __init__(self, config: Config):
        self.config = config

    def get_name(self):
        return 'debug'

    def add_parser(self, subparsers):
        subparsers.add_parser('debug',
                              description='Start project dependencies so it could be run on host machine',
                              help='start project dependencies')

    def do(self, args: Namespace):
        commands = [
            'docker build -t {long_name}/db:latest --progress plain ./db/'.format(long_name=self.config.long_name) if self.config.database else None,
            'docker build -t {long_name}/app:latest --progress plain .'.format(long_name=self.config.long_name) ,
            'docker compose -f compose/base.yml -f compose/debug.yml -p {short_name}_local up --build --force-recreate --remove-orphans'.format(short_name=self.config.short_name)
        ]
        env_vars = {
            'ENV': 'local',
        }

        run_commands(commands, env_vars)

    # TODO: maybe attach to empty debug container
    # docker exec -i --tty $$(docker ps -f name=toxic_local_app --quiet) /bin/bash
