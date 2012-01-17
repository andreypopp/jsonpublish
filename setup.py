from setuptools import setup
from setuptools import find_packages

version = "0.1"

setup(
    name="jsonpublish",
    version=version,
    description="Publish Python object as JSON documents",
    author="Andrey Popp",
    author_email="8mayday@gmail.com",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    zip_safe=False)
