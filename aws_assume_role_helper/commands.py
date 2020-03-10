"""
Commands to manage and assume IAM roles
"""

import os
import configparser
import yaml
import boto3


class AWSAssumeRoleHelper(object):
    CONFIG_DIRECTORY = os.path.join(os.environ['HOME'], '.assume')
    CONFIG_FILENAME = os.path.join(CONFIG_DIRECTORY, 'config.yaml')
    CREDENTIALS_FILENAME = os.path.join(os.environ['HOME'], '.aws', 'credentials')

    AWS_PROFILE_TEMPORARY_NAME = 'default-assume-temp'

    config = {}

    def __init__(self):
        if not os.path.isdir(self.CONFIG_DIRECTORY):
            os.makedirs(self.CONFIG_DIRECTORY)

        if not os.path.isfile(self.CONFIG_FILENAME):
            open(self.CONFIG_FILENAME, 'a').close()

        with open(self.CONFIG_FILENAME, 'r') as stream:
            self.config = yaml.load(stream)

            if self.config is None:
                self.config = {}

    def _dump_config(self):
        with open(self.CONFIG_FILENAME, 'w', encoding='utf8') as contents:
            yaml.dump(self.config, contents, default_flow_style=False, allow_unicode=True)

    def add(self, name, role_arn, profile):
        self.config[name] = {'role_arn': role_arn}

        if profile:
            self.config[name]['profile'] = profile

        self._dump_config()

        return "Added role '{0}' to the configuration. You can now assume this "\
            "role with:\n\nassume switch {0}".format(name)

    def remove(self, name):
        self.config.pop(name)

        self._dump_config()

        return "Role '{}' removed from the configuration. Please note that if " \
            "you are currently assuming this role, you still need to clear this " \
            "with:\n\nassume clear".format(name)

    def list(self):
        return yaml.dump(self.config, default_flow_style=False)

    def switch(self, name):
        self.clear()

        role_arn = self.config[name]['role_arn']

        if 'profile' in self.config[name]:
            session = boto3.session.Session(profile_name=self.config[name]['profile'])
        else:
            session = boto3.session.Session()

        sts = session.client('sts')

        response = sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName=name,
        )

        access_key_id = response['Credentials']['AccessKeyId']
        secret_access_key = response['Credentials']['SecretAccessKey']
        session_token = response['Credentials']['SessionToken']

        config_credentials = configparser.ConfigParser()
        config_credentials.read(self.CREDENTIALS_FILENAME)

        credentials_file = open(self.CREDENTIALS_FILENAME, 'w')

        sections = config_credentials.sections()

        if self.AWS_PROFILE_TEMPORARY_NAME not in sections:
            config_credentials.add_section(self.AWS_PROFILE_TEMPORARY_NAME)

            for key in config_credentials.options('default'):
                config_credentials.set(self.AWS_PROFILE_TEMPORARY_NAME, key, config_credentials.get('default', key))

        config_credentials.set('default', 'aws_access_key_id', access_key_id)
        config_credentials.set('default', 'aws_secret_access_key', secret_access_key)
        config_credentials.set('default', 'aws_session_token', session_token)

        config_credentials.write(credentials_file)
        credentials_file.close()

        return "Now assuming role '{}".format(name)

    def clear(self, echo=True):
        config_credentials = configparser.ConfigParser()
        config_credentials.read(self.CREDENTIALS_FILENAME)

        sections = config_credentials.sections()

        if self.AWS_PROFILE_TEMPORARY_NAME in sections:

            if 'default' not in sections:
                config_credentials.add_section('default')

            for key in config_credentials.options(self.AWS_PROFILE_TEMPORARY_NAME):
                config_credentials.set('default', key, config_credentials.get(self.AWS_PROFILE_TEMPORARY_NAME, key))
            config_credentials.remove_option('default', 'aws_session_token')

            config_credentials.remove_section(self.AWS_PROFILE_TEMPORARY_NAME)

            credentials_file = open(self.CREDENTIALS_FILENAME, 'w')
            config_credentials.write(credentials_file)
            credentials_file.close()

            return "Cleared previous role that was assumed"

        return "No role was assumed; nothing to clear"
