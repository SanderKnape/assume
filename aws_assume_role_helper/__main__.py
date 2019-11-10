#!/usr/bin/env python
"""Main entrypoint for CLI application"""
from __future__ import print_function
import argparse
import re

from aws_assume_role_helper import __version__
from aws_assume_role_helper.commands import AWSAssumeRoleHelper


def main():
    arguments = parse_arguments()

    commands = AWSAssumeRoleHelper()

    if arguments.command == 'add':
        print(commands.add(arguments.name, arguments.role_arn, arguments.profile))
    elif arguments.command == 'remove':
        print(commands.remove(arguments.name))
    elif arguments.command == 'list':
        print(commands.list())
    elif arguments.command == 'switch':
        print(commands.switch(arguments.name))
    elif arguments.command == 'clear':
        print(commands.clear())


def parse_arguments():

    parser = argparse.ArgumentParser(description='Helper to assume IAM roles in AWS')
    parser.add_argument('--version', '-v', action='version', version=__version__)

    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add an IAM role')
    add_parser.add_argument('name', help='Name of the role to add')
    add_parser.add_argument('--role-arn', required=True, type=iam_role_type, help='The role ARN to assume')
    add_parser.add_argument('--profile', default='', help='The profile to use when assuming the role (optional)')

    remove_parser = subparsers.add_parser('remove', help='Remove an IAM role')
    remove_parser.add_argument('name', help='Name of the role to remove')

    subparsers.add_parser('list', help='List added IAM roles')

    switch_parser = subparsers.add_parser('switch', help='Assume one of the added IAM roles')
    switch_parser.add_argument('name', help='Name of the role to assume')

    subparsers.add_parser('clear', help='Clear any currently assumed role')

    return parser.parse_args()


def iam_role_type(role_arn):
    regex = r'^arn:aws:iam::[0-9]{12}:role\/[a-zA-Z0-9_+=,.@-]*$'

    if not re.match(regex, role_arn):
        raise "Not a valid IAM ARN"
    return role_arn


if __name__ == '__main__':
    main()
