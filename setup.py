from setuptools import setup
from setuptools import find_packages

version = "0.1"

setup(
    name="jsonpublish",
    version="0.1",
    description="Publish Python object as JSON documents",
    author="Andrey Popp",
    author_email="8mayday@gmail.com",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    test_suite="jsonpublish.tests",
    install_requires=[
        "zope.proxy >= 3.6.1",
        "zope.interface >= 3.8.0",
        "repoze.lru >= 0.4",
    ],
    zip_safe=False)
