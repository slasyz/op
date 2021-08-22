import os
import sys

from op.config import Config
from op.run import run_commands, get_output, run_command


class Docker:
    def __init__(self, config: Config):
        self.config = config

    def assure(self, env: str):
        if env not in ('local', 'tests'):
            context_out = get_output('docker context ls | grep "^{}_{}\s" || true'.format(self.config.short_name, env))
            if not context_out:
                print('Please create context: \n$ docker context create {}_{} --docker "host=ssh://user@hostname"'.format(self.config.short_name, env))
                sys.exit(1)

        context_param = ''
        if env not in ('local', 'tests'):
            context_param = ' --context={}_{}'.format(self.config.short_name, env)

        infra = get_output('docker{} network ls -f name=infra | grep infra || true'.format(context_param))
        if not infra:
            run_command('docker{} network create --attachable infra'.format(context_param))

    def get_context_addr(self, name: str) -> str:
        return get_output('docker context inspect {} -f "{{{{.Endpoints.docker.Host}}}}"'.format(name))

    def deploy(self, env: str):
        context_name = '{}_{}'.format(self.config.short_name, env)
        env_vars = {**os.environ, **{
            'ENV': env,
        }}

        commands = [
            'docker --context {context_name} build -t {long_name}/db:latest --progress plain ./db/'.format(context_name=context_name, long_name=self.config.long_name) if self.config.database else None,
            'docker --context {context_name} build -t {long_name}/app:latest --progress plain .'.format(context_name=context_name, long_name=self.config.long_name),
            'docker --context {context_name} compose -f compose/base.yml -f compose/{env}.yml -p {short_name}_{env} up -d --build --force-recreate --remove-orphans -t 2'.format(
                context_name=context_name,
                env=env,
                short_name=self.config.short_name
            ),
        ]
        run_commands(commands, env_vars)

    def integration_tests(self):
        env_vars = {**os.environ, **{
            'ENV': 'tests',
        }}

        commands = [
            'docker compose -f compose/base.yml -f compose/tests.yml -p {}_tests down -t 2'.format(self.config.short_name),
            'docker volume rm -f {}_tests_postgres_data'.format(self.config.short_name),
            'docker build -t {}/db:latest --progress plain ./db/'.format(self.config.long_name) if self.config.database else None,
            'docker build -t {}/app:latest --progress plain .'.format(self.config.long_name),
            'docker compose -f compose/base.yml -f compose/tests.yml -p {}_tests up -d --build --force-recreate --remove-orphans -t 2'.format(self.config.short_name),
            'docker compose -f compose/base.yml -f compose/tests.yml -p {}_tests exec app /bin/bash -c "make test.all"'.format(self.config.short_name),
            'docker compose -f compose/base.yml -f compose/tests.yml -p {}_tests down -t 2'.format(self.config.short_name),
        ]
        run_commands(commands, env_vars)
