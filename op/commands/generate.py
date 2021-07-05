from argparse import Namespace

from op.generator import Generator


class Generate:
    def __init__(self, generator: Generator):
        self.generator = generator

    def get_name(self):
        return 'generate'

    def add_parser(self, subparsers):
        subparsers.add_parser('generate',
                              description='Create or update generated files.',
                              help='create or update generated files')

    def do(self, args: Namespace):
        self.generator.generate_everything()
