import logging
import os
import sys

from rpyc.core.service import SlaveService

from consts import (MAIN_LOGGER_NAME, SERVER_LOGGER_NAME, SERVICE_PORT,
                    SERVICE_USE_TCP_ENV_VAR)

should_use_tcp = os.environ.get(SERVICE_USE_TCP_ENV_VAR, None)

# Note for future readers, this is cosidered really bad practice
# in general, you should avoid importing packages inside if statements,
# but I really could not think of a better soultion
if should_use_tcp:
    from rpyc.utils.server import ThreadedServer as RPYCServer
else:
    from vmci_server import VMCISocketServer as RPYCServer


def get_server(root_logger: logging.Logger):
    server_logger = root_logger.getChild(SERVER_LOGGER_NAME)
    try:
        server = RPYCServer(
            SlaveService,
            port=SERVICE_PORT,
            logger=server_logger,
        )
        return server
    except Exception:
        root_logger.exception('Failed to create server')
        raise


def start_server(server: RPYCServer, logger: logging.Logger):
    try:
        logger.info(f'Starting server on {server.host}:{server.port}')
        server.start()
    except Exception:
        logger.exception('Closing server after unexpected exception')
        server.close()


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger(MAIN_LOGGER_NAME)
    server = get_server(logger)
    start_server(server, logger)


if __name__ == '__main__':
    main()
