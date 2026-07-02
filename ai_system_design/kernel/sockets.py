from enum import IntEnum

import ai_system_design.kernel._sockets as _sockets
from ai_system_design.kernel._sockets import * # type: ignore 


class AdressFamily(IntEnum):
    ADDRESS_FAMILY_INET = 1


ADDRESS_FAMILY_INET: Final = AdressFamily.ADDRESS_FAMILY_INET

class SocketCategory(IntEnum):
    SOCKET_STREAM = 1


SOCKET_STREAM: Final = SocketCategory.SOCKET_STREAM

class Socket(_sockets.Socket):
    def __init__(self, socket_family: int = -1, socket_category: int = -1):
        self.socket_family = socket_family
        self.socket_category = socket_category
        
