# How to connect to an RPyC serice over VSock
import socket

import rpyc
from rpyc.core.protocol import Connection
from rpyc.core.stream import SocketStream

TEST_PORT = 8080


def get_stream(host: int, port: int) -> SocketStream:
    vmci_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    vmci_socket.connect((host, port))
    stream = SocketStream(vmci_socket)
    return stream


def connect(host: int, port: int) -> Connection:
    stream = get_stream(host, port)
    connection = rpyc.classic.connect_stream(stream)
    return connection


def main():
    connection = connect(socket.VMADDR_CID_HOST, TEST_PORT)
    connection.ping()
    connection.close()


if __name__ == '__main__':
    main()
