import socket

from rpyc.utils.server import ThreadedServer

ANY_CID = -1


class VMCISocketServer(ThreadedServer):

    def __init__(self, *args, port: int = None, **kwargs):
        super().__init__(*args, port=port, **kwargs)
        # Closing the default listener created by threaded server
        self.listener.close()
        # Creating a new listener using VSOCK as the protocol
        self.listener = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.listener.bind((ANY_CID, port))
        sock_details = self.listener.getsockname()
        self.host, self.port = sock_details[0], sock_details[1]
