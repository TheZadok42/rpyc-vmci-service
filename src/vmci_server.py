import fcntl
import socket
import struct

from rpyc.utils.server import ThreadedServer

from consts import ANY_CID, CID_STRUCT_FORMAT, UNIX_VSOCK_DEVICE_PATH


def _get_local_vsock_device_path():
    # TODO: add windows support
    return UNIX_VSOCK_DEVICE_PATH


def get_local_cid():
    local_vsock_device_path = _get_local_vsock_device_path()
    buffer_string = ' ' * 4
    with open(local_vsock_device_path, 'rb') as vsock_device:
        raw_result = fcntl.ioctl(vsock_device,
                                 socket.IOCTL_VM_SOCKETS_GET_LOCAL_CID,
                                 buffer_string)
    # struct alaways returns a tuple, we only need the first number
    return struct.unpack(CID_STRUCT_FORMAT, raw_result)[0]


class VMCISocketServer(ThreadedServer):

    def __init__(self, *args, port: int = None, **kwargs):
        super().__init__(*args, port=port, **kwargs)
        # Closing the default listener created by threaded server
        self.listener.close()
        # Creating a new listener using VSOCK as the protocol
        # TODO: add windows support
        self.listener = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.listener.bind((ANY_CID, port))
        # The original ThreadedServer uses getsockname
        # to get the host and the port
        # This doesn't return the right host for VSOCK, so we get the local cid
        self.host = get_local_cid()
        self.port = port
