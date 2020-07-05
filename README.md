# pygate
Python interface to [Textile](https://textile.io/)'s [Powergate](https://docs.textile.io/powergate/) [Filecoin](https://filecoin.io/) API

This a [HackFS](https://hackfs.com/) project.

![concept_diagram](pygate_concept.png)

1) Create a Python gRPC client for the Powergate API.
2) Create a Flask application that reads and writes to IPFS & Filecoin using this client.
3) Drop the Flask app in an Electron shell and create a cross-platform, drag-and-drop desktop app that moves local files to and from IPFS/Filecoin.
4) Add smart contracts to the desktop app to provide escrow funding for storage deals.
