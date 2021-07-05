from argparse import Namespace


class Help:
    def get_name(self):
        return 'help'

    def add_parser(self, subparsers):
        subparsers.add_parser('help',
                              description='Show op command help.',
                              help='show help')

    def do(self, args: Namespace):
        pass  # Nothing to do.  This class is used only for consistent subparsers.add_parser(...) call.
