from setuptools import setup
from setuptools import find_packages

setup(
    name="jsonpublish",
    version="0.1.2",
    description="Publish Python object as JSON documents",
    long_description=open("README").read() + "\n\n" + open("CHANGES").read(),
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
