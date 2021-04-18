#!/usr/bin/env python3
import os
import subprocess
from datetime import date
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version(module):
    version = date.today().strftime('%Y-%m')
    git_tag = "0.0"
    git_commits = "0"
    suffix = "dev"
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).rstrip().decode('utf8')
        git_describe = subprocess.check_output(["git", "describe", "--long"]).rstrip().decode('utf8')
        git_tag = git_describe.split('-')[0]
        git_commits = git_describe.split('-')[1]
        if branch == 'master':
            suffix = ''
        else:
            suffix = 'dev'
        print(branch, git_tag, git_commits, suffix)
        version = '{}.{}{}'.format(git_tag, git_commits, suffix)
    except (subprocess.CalledProcessError, OSError) as e:
        print('git not installed', e)
    try:
        fp = open('{}/__init__.py'.format(module), 'w')
        fp.write('__version__ = [{}, {}, "{}"]'.format(git_tag.replace('.', ','), git_commits, suffix))
        fp.close()
    except Exception:
        print('ERROR opening {}/__init__.py'.format(module), os.curdir)
    return version

module = 'apistats'

setup(
    name='apistats',
    description='Simple django module with a middleware to track calls to django backend.',
    python_requires='>3.7.0',
    version=get_version(module),
    author='Frédéric MEUROU',
    author_email='fm@peabytes.me',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    install_requires=[
        "Django~=3.0",
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Information Technology",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
        "License :: OSI Approved :: MIT License",
    ],
    py_modules=[
        'apistats',
    ],
)
