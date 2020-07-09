# pygate gRPC client

![Tests](https://github.com/pygate/pygate-gRPC/workflows/Tests/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python interface to [Textile](https://textile.io/)'s [Powergate](https://docs.textile.io/powergate/) [Filecoin](https://filecoin.io/) API

This a [HackFS](https://hackfs.com/) project. 

The gRPC client is Phase 1 in the concept diagram below. It is intended to serve as a stand-alone component that can be used in other projects.

See the project [wiki](https://github.com/pygate/gRPC-client/wiki) for additional resources and project status.

![concept_diagram](pygate_concept.png)

1) Create a Python gRPC client for the Powergate API.
2) Create a Flask application that reads and writes to IPFS & Filecoin using this client.
3) Drop the Flask app in an Electron shell and create a cross-platform, drag-and-drop desktop app that moves local files to and from IPFS/Filecoin.
4) Add Ethereum smart contract(s) to the desktop app to provide escrow funding for storage deals.

## Getting Started

You can get started using `pygate_grpc` by installing it through the test PyPi repository.

```
pip install --index-url https://test.pypi.org/simple/ pygate_grpc
```

> The package will be released to main PyPi repository after the first stable release.

## Usage

The main component of the package is the `PowerGateClient` class. 

Here is a basic usage example of the pygate_grpc:

```python
from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002")

healthcheck = client.health.check()
```

Simple as that!

Examples of more elaborated usage can be found in the [examples](./examples/)  folder.

## Development

To setup your development environment make sure you have the following software:

- [Python](https://www.python.org/downloads/release/python-370/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [pipenv](https://pypi.org/project/pipenv/) ( or run `pip install pipenv`)

## Install dependencies

Runtime and development dependencies can be installed in a new virtual environment automatically by running:

NOTE: The `--dev` flag can be ommited if you only need runtime dependencies
```
pipenv install --dev
```

### **Using the virtual environment**

To run any command through pipenv's virtual environment you can spawn a new virtual environment shell by running:

```
pipenv shell
```

## Code Style

This project uses [black](https://pypi.org/project/black/) code formatter for consistency. Since the are not any precommit hooks defined in the repository yet please format your code before opening a pull request. 

Automatic formatting can be performed by running:
```
pipenv run format
```

## Running the tests

Currently the test suite is very minimal. Full Testing is in the project's roadmap but it will be developed only if the timeframe of the Hackathon allows to do so.

### **Integration Tests**

Integration tests spin up a localnet using the official script from powergate repository and the test cases are run using that network. By implication, to run the test make sure you have the following dependencies installed:

- docker-compose
- docker
- git

To run the integration tests run:

```
pipenv run integration-test
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/apogiatzis/powsolver/tags). 

To automatically bump the version of the package run:
```
bump2version major|minor|patch setup.py
```

Finally, to push the new version to git and trigger a new release action it is necessary to add the `--tags` flag at the time of pushing. i.e.:
```
git push origin main --tags
```

## Authors

* **Antreas Pogiatzis** - *Initial scaffolding* 
* **Wang Ge**
* **Antreas Pogiatzis**


See also the list of [contributors](https://github.com/pygate/pygate-gRPC/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
