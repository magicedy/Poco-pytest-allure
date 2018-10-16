# coding=utf-8

import os
from setuptools import setup, find_packages


def parse_requirements(filename='requirements.txt'):
    """ load requirements from a pip requirements file. (replacing from pip.req import parse_requirements)"""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if os.path.exists('requirements.txt'):
    reqs = parse_requirements()
else:
    reqs = []

setup(
    name='poco-pytest-allure',
    version='0.0.1',
    description='A test automation project using poco, pytest and allure.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    license='MIT License'
)
