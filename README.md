# RPyC over VSOCK

This small python repo is a POC for creating an RPyC service over VSOCK.

## VSock

[VSock](https://www.man7.org/linux/man-pages/man7/vsock.7.html) is a protocol meant for communications from a host to a virtual guest without a network connection.  
This allows to connect to services on completely "off the grid" machines.

## RPyC

[Remote Python Call](https://rpyc.readthedocs.io/en/latest/) is a python package which allows remote python execution over the network. In this code base, we use the classic protocol to allow more control. This is considered **unsafe**, so use with caution.
