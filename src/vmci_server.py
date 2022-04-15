import fcntl
import socket
import struct

from rpyc.utils.server import ThreadedServer

ANY_CID = -1

VSOCK_DEVICE_PATH = '/dev/vsock'


def get_local_cid():
    with open(VSOCK_DEVICE_PATH, 'rb') as vsock_device:
        raw_result = fcntl.ioctl(vsock_device,
                                 socket.IOCTL_VM_SOCKETS_GET_LOCAL_CID,
                                 ' ' * 4)
    return struct.unpack('<L', raw_result)[0]


class VMCISocketServer(ThreadedServer):

    def __init__(self, *args, port: int = None, **kwargs):
        super().__init__(*args, port=port, **kwargs)
        # Closing the default listener created by threaded server
        self.listener.close()
        # Creating a new listener using VSOCK as the protocol
        self.listener = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.listener.bind((ANY_CID, port))
        # The original ThreadedServer uses getsockname to get the host and the port
        # This doesn't return the right host for VSOCK
        self.host = get_local_cid()
        self.port = port
