import os
from setuptools import setup

with open("requirement.txt") as f:
    install = f.read().splitlines()
setup(
    install_requires=install
)