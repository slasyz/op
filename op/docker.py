import os

from op.config import Config
from op.run import run


class Docker:
    def __init__(self, config: Config):
        self.config = config

    def assure(self):
        # TODO: check if networks and contexts are created.
        #  Ask to create context manually; create network automatically.
        pass

    def deploy(self, env: str):
        context_name = '{}_{}'.format(self.config.short_name, env)
        env_vars = {**os.environ, **{
            'ENV': env,
        }}

        commands = (
            ('docker', '--context', context_name, 'build', '-t', '{}/db:latest'.format(self.config.long_name), '--progress', 'plain', './db/'),
            ('docker', '--context', context_name, 'build', '-t', '{}/db:latest'.format(self.config.long_name), '--progress', 'plain', '.'),
            ('docker', '--context', context_name, 'compose',
                '-f', 'compose/base.yml', '-f', 'compose/{}.yml'.format(env),
                '-p', '{}_{}'.format(self.config.short_name, env),
                'up', '-d', '--build', '--force-recreate', '--remove-orphans', '-t', '2'),
        )
        run(commands, env_vars)

    def integration_tests(self):
        env_vars = {**os.environ, **{
            'ENV': 'tests',
        }}

        commands = (
            ('docker', 'compose',
                '-f', 'compose/base.yml', '-f', 'compose/tests.yml',
                '-p', '{}_tests'.format(self.config.short_name),
                'down', '-t', '2'),
            ('docker', 'volume', 'rm', '-f', '{}_tests_postgres_data'.format(self.config.short_name)),
            ('docker', 'build', '-t', '{}/db:latest'.format(self.config.long_name), '--progress', 'plain', './db/'),
            ('docker', 'build', '-t', '{}/db:latest'.format(self.config.long_name), '--progress', 'plain', '.'),
            ('docker', 'compose',
                '-f', 'compose/base.yml', '-f', 'compose/tests.yml',
                '-p', '{}_tests'.format(self.config.short_name),
                'up', '-d', '--build', '--force-recreate', '--remove-orphans', '-t', '2'),
            ('docker', 'compose',
                '-f', 'compose/base.yml', '-f', 'compose/tests.yml',
                '-p', '{}_tests'.format(self.config.short_name),
                'exec', 'app', '/bin/bash', '-c', 'make test.all'),
            ('docker', 'compose',
                '-f', 'compose/base.yml', '-f', 'compose/tests.yml',
                '-p', '{}_tests'.format(self.config.short_name),
                'down', '-t', '2'),
        )
        run(commands, env_vars)
