# pygate gRPC client
A Python interface to [Textile](https://textile.io/)'s [Powergate](https://docs.textile.io/powergate/) [Filecoin](https://filecoin.io/) API

This a [HackFS](https://hackfs.com/) project. 

The gRPC client is Phase 1 in the concept diagram below. It is intended to serve as a stand-alone component that can be used in other projects.

See the project [wiki](https://github.com/pygate/gRPC-client/wiki) for additional resources and project status.

![concept_diagram](pygate_concept.png)

1) Create a Python gRPC client for the Powergate API.
2) Create a Flask application that reads and writes to IPFS & Filecoin using this client.
3) Drop the Flask app in an Electron shell and create a cross-platform, drag-and-drop desktop app that moves local files to and from IPFS/Filecoin.
4) Add Ethereum smart contract(s) to the desktop app to provide escrow funding for storage deals.
