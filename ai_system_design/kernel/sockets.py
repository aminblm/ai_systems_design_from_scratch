# sockets.py

import ai_system_design.kernel._sockets as _sockets
from _sockets import * # type: ignore 


class Socket(_sockets.Socket):
    def __init__(self, socket_family: int = -1, socket_type: int = -1):
        self.socket_family = socket_family
        self.socket_type = socket_type
        
