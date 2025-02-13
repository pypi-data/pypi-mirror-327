from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory,'README.md'),encoding='UTF-8') as f:
    long_description = f.read()

setup (
    name = "imzML_Writer",
    version = "0.0.1",
    url = "https://github.com/VIU-Metabolomics/imzML_Writer",
    author = "Joseph Monaghan",
    author_email = "Joseph.Monaghan@viu.ca",
    description = "User friendly writing of imzML mass spectrometry imaging files from continuous MSI data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],

)