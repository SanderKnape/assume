# AWS Assume Role Helper
[![Build Status](https://travis-ci.org/SanderKnape/aws-assume-role-helper.svg?branch=master)](https://travis-ci.org/SanderKnape/aws-assume-role-helper)

The `aws-assume-role-helper` is a simple CLI utility that makes it easier to switch between different AWS roles. This is helpful when you work with different AWS accounts or users. In addition, this utility is helpful when you develop AWS resources locally (such as an application that will run on EC2 or when running a Lambda function locally using [AWS SAM](https://github.com/awslabs/aws-sam-cli)). You can easily switch to a role that your EC2 instance / Lambda function will assume in AWS.

What this command actually does is change your AWS credentials file (`~/.aws/credentials`). If there is a `default` role in there, it will be stored in a temporary role. The assumed role is then passed in the `default` role, so you can immediately start using it.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Alternatives](#alternatives)

## Prerequisites

[Install Python](https://www.python.org/downloads/). Versions 3.5 and 3.6 are supported.

## Installation

Use [pip](https://pypi.org/project/pip/) to install the `aws-assume-role-helper':

```bash
pip install aws-assume-role-helper
```

*Optional*: create an alias to make it even easier to switch between roles. Add the following to your shell login file (e.g. `~/.bashrc` or `~/.zshrc`):

```bash
alias assume=aws-assume-role-helper
```

Run the following to show all available commands:

```bash
aws-assume-role-helper --help
```

## Usage

Add a new role to assume as follows:

```bash
aws-assume-role-helper add [rolename] --role-arn [arn] --profile [profile]
```

Specifying the profile is optional. When you don't specify this, the default profile is used. The following would `add` a new role "myrole" to be assumed:

```bash
aws-assume-role-helper add myrole --role-arn arn:aws:iam::012345678912:role/myrole
```

You can now `assume` this role as follows:

```bash
aws-assume-role-helper assume myrole
```

The `aws-assume-role-helper` keeps a configuration file in `~/.aws-assume-role-helper/config.yaml`. You can list the contents of the current configuration with the following file:

```bash
aws-assume-role-helper list
```

When you want to switch back to your initial default role, you can `clear` the assumed role as follows:

```bash
aws-assume-role-helper clear
```

To `remove` a role to be assumed, run the following command:

```bash
aws-assume-role-helper remove myrole
```

This command grabs the `default` role that was stored in a temporary location when running the `assume` command. These credentials are then put back in the `default` role.

## Alternatives

I'm aware that a number of alternatives already exist with similar functionality. The reason I decided to build my own functionality is because I wasn't be able to find an existing option that combines all of the following features:

* Easy switching using shortcuts
* Easily remove the temporarry role and switch back to the original one
