from argparse import Namespace
from urllib.parse import urlparse

from op.config import Config
from op.docker import Docker
from op.run import run_command


class Ports:
    def __init__(self, config: Config, deployer: Docker):
        self.config = config
        self.deployer = deployer

    def get_name(self):
        return 'ports'

    def add_parser(self, subparsers):
        subparsers.add_parser('ports',
                              description='Forward ports.',
                              help='forward ports')

    def do(self, args: Namespace):
        command = 'ssh'
        context_name = '{}_prod'.format(self.config.short_name)
        url = self.deployer.get_context_addr(context_name)

        parsed_url = urlparse(url)
        if parsed_url.scheme != 'ssh':
            raise Exception('context {} must have SSH address, but has "{}"'.format(context_name, parsed_url.scheme))

        for service, port in self.config.ports['prod'].items():
            # TODO: output smth like "http://localhost:30120/messages" to help open endpoint
            print('mapping {hostname}:{port} to localhost:{port}'.format(hostname=parsed_url.hostname, port=port))
            command += ' -L {port}:localhost:{port}'.format(port=port)

            if service == 'db':
                print('$ psql -h localhost -p {port} -U {short_name} -d {short_name}'.format(port=port, short_name=self.config.short_name))

        command += ' {} "sleep infinity"'.format(parsed_url.netloc)
        run_command(command)
