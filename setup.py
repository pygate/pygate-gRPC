# read the contents of your README file
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    install_requires=[
        "deprecated==1.2.11",
        "grpc-powergate-client==2.1.0",
        "grpcio==1.35.0",
        "mypy-extensions==0.4.3",
        "protobuf==3.18.3",
        "six==1.15.0",
        "wrapt==1.12.1",
    ],
    name="pygate_grpc",
    version="2.0.0",
    description="A Python interface to Textile's Powergate Filecoin API",
    url="https://github.com/pygate/pygate-gRPC",
    author="Pygate Team",
    author_email="info@pygate.com",
    license="MIT",
    packages=["pygate_grpc", "pygate_grpc.admin"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
