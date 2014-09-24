from setuptools import setup
from setuptools import find_packages

setup(
    name="jsonpublish",
    version="0.1.3",
    description="Publish Python object as JSON documents",
    long_description=open("README").read() + "\n\n" + open("CHANGES").read(),
    author="Andrey Popp",
    author_email="8mayday@gmail.com",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    test_suite="jsonpublish.tests",
    install_requires=[
        "zope.proxy >= 4.1.4, < 5.0.0",
        "zope.interface >= 4.1.1, < 5.0.0",
        "repoze.lru >= 0.6, < 0.7",
    ],
    zip_safe=False)
