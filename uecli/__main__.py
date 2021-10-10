import argparse
from campussquare.cli import get_parser, parse_args_with_handler
from .authenticator import UECCampusSquareAuthenticator
from . import info

campussquare_commands = ['syllabus', 'grades']


def main():
    parser = argparse.ArgumentParser('uecli')
    parser.add_argument('--version', '-V', action='version', version=f'{info.name} {info.version}')
    parser.add_argument('command', choices=[*campussquare_commands])
    parser.add_argument('args', nargs='*')
    args, _ = parser.parse_known_args()

    if args.command in campussquare_commands:
        # Campus Square commands
        parser = get_parser(authenticator=UECCampusSquareAuthenticator())
        parse_args_with_handler(parser)
    else:
        # Other commands
        raise NotImplementedError()
