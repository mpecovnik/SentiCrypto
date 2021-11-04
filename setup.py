import os
import re

from setuptools import find_packages, setup


def parse_requirements(file):
    with open(os.path.join(os.path.dirname(__file__), file)) as req_file:
        return [line.strip() for line in req_file if "/" not in line]


def get_version():
    with open(os.path.join(os.path.dirname(__file__), "secr", "__init__.py")) as file:
        return re.findall('__version__ = "(.*)"', file.read())[0]


setup(
    name="secr",
    python_requires=">=3.8",
    version=get_version(),
    description="Cryptocurrency Sentiment Analysis",
    url="https://github.com/mpecovnik/SentiCrypto",
    author="Matic Pečovnik",
    author_email="matic.pecovnik@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements("requirements.txt"),
    extras_require={"DEV": parse_requirements("requirements-dev.txt")},
    zip_safe=False,
)
