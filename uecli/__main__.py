import sys
import argparse
import campussquare.cli
import limedio.cli
from .authenticator import UECCampusSquareAuthenticator, UECLibraryAuthenticator
from . import info

campussquare_commands = ['syllabus', 'grades']
library_command = 'library'


def main():
    parser = argparse.ArgumentParser('uecli')
    parser.add_argument('--version', '-V', action='version', version=f'{info.name} {info.version}')
    parser.add_argument('command', choices=[*campussquare_commands, library_command])
    parser.add_argument('args', nargs='*')
    args, _ = parser.parse_known_args()

    if args.command in campussquare_commands:
        # Campus Square commands
        print(sys.argv)
        parser = campussquare.cli.get_parser(authenticator=UECCampusSquareAuthenticator())
        campussquare.cli.parse_args_with_handler(parser)
    elif args.command == library_command:
        del sys.argv[1]

        # Library Command
        parser = limedio.cli.get_parser(authenticator=UECLibraryAuthenticator())
        limedio.cli.parse_args_with_handler(parser)
    else:
        # Other commands
        raise NotImplementedError()
