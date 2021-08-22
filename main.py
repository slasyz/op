#!/usr/bin/env python3


import argparse
import os

from op.commands.backup import Backup
from op.commands.debug import Debug
from op.commands.deploy import Deploy
from op.commands.help import Help
from op.commands.init import Init
from op.commands.logs import Logs
from op.commands.ports import Ports
from op.commands.stat import Stat
from op.commands.tests import Tests
from op.commands.generate import Generate
from op.config import parse_config
from op.docker import Docker
from op.generator import Generator


def main():
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(dest='subcommand',
                                       metavar='SUBCOMMAND')

    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

    commands = [
        Help(),
        Init(templates_dir),
    ]

    try:
        config = parse_config()
        deployer = Docker(config)
        generator = Generator(config, templates_dir)

        commands.extend([
            Generate(generator),
            Deploy(config, deployer),
            Debug(config),
            Tests(config, deployer),
            Stat(config),
            Logs(config),
            Ports(config, deployer),
            Backup(config),
        ])
    except FileNotFoundError:
        print('file not found')
        # print('op utility must be started inside a dir containing op.toml.  To create such file, run "op init".\n')

    for command in commands:
        command.add_parser(subparsers)

    args = parser.parse_args()
    if args.subcommand == 'help':
        parser.print_help()
        return

    for command in commands:
        if args.subcommand == command.get_name():
            command.do(args)
            break
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
