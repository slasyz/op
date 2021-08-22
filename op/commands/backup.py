import sys
from argparse import Namespace
from time import strftime

from op.config import Config
from op.run import get_output, run_commands


class Backup:
    def __init__(self, config: Config):
        self.config = config

    def get_name(self):
        return 'backup'

    def add_parser(self, subparsers):
        subparsers.add_parser('backup',
                              description='Backup database.',
                              help='backup database')

    def do(self, args: Namespace):
        if not self.config.database:
            print('Nothing to backup.')
            sys.exit(1)

        filename = strftime('./backups/backup-%Y%m%d-%H%M%S-container.sql.gz')
        container = get_output('docker --context={short_name}_prod ps -f name={short_name}_prod_db --quiet'.format(
            short_name=self.config.short_name,
        ))

        commands = [
            'docker --context={short_name}_prod exec -i {container} pg_dump --data-only --inserts -h localhost -d {short_name} -U {short_name} | gzip > {filename}'.format(
                short_name=self.config.short_name,
                container=container,
                filename=filename,
            ),
            'du -sh ./backups/*',
        ]
        run_commands(commands)
