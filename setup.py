from setuptools import setup
from aws_assume_role_helper import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aws-assume-role-helper',
    python_requires='>3.5.2',
    version=__version__,
    description='Helper to easily assume IAM roles in AWS',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/SanderKnape/aws-assume-role-helper',
    author='Sander Knape',
    author_email='s.knape88@gmail.com',
    license='MIT',
    packages=['aws_assume_role_helper'],
    entry_points={
        'console_scripts': [
            'aws-assume-role-helper = aws_assume_role_helper.__main__:main'
        ]
    },
    install_requires=[
        'pyyaml~=3.12',
        'boto3~=1.5'
    ],
    extras_require={
        'dev': [
            'flake8',
            'pylint'
        ]
    },
    zip_safe=False
)
