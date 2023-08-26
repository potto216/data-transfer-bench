# Overview
This repository is a collection of simple applications designed to test and benchmark data transfer over various communication links. It contains several simple Python programs that use sockets or [ZMQ](https://zeromq.org/languages/python/) to provide functionality. The code is meant to be modified to suit one's needs. Most files come in pairs: a server and a client. The two pairs are:

- The zmq_hello_world pair, which shows basic ZMQ functionality.
- The zmq_run_command pair, which demonstrates how a client on a different machine can be used to run a program on the server.
- The udp_pkt pair, which is useful when needing to create data flow on a communication link with known data, such as when capturing wireless traffic.

# Details
Please refer to the specific programs for information on how to use them. If you intend to use the programs between two machines or between a virtual machine and a host, you may need to adjust your firewall settings. This is especially true if one of the computers is running Windows.

# Information on Pyzmq
- Github: https://github.com/zeromq/pyzmq
- Docs: https://pyzmq.readthedocs.io/en/latest/
- Guide: http://zguide.zeromq.org/py:all
- PyPI: https://pypi.org/project/pyzmq/

# How to Install Pyzmq
You can install Pyzmq using pip or conda depending on your system:

- `pip install pyzmq`
- `conda install -c conda-forge pyzmq`
