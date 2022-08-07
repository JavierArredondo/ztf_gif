#!/usr/bin/env python

from setuptools import find_packages, setup
from ztf_gif import __version__

with open("requirements.txt") as f:
    required_packages = f.readlines()

setup(
    name="ztf_gif",
    version=__version__,
    description="",
    author="JavierArredondo",
    author_email="javier.arredondo.c@usach.cl",
    include_package_data=True,
    packages=find_packages(),
    install_requires=required_packages,
    build_requires=required_packages,
    project_urls={
        "Github": "https://github.com/JavierArredondo/ztf_gif",
        "Documentation": "",
    },
)
