from typing import Final, Any, SupportsIndex
from typing_extensions import disjoint_base, TypeAlias

from ai_system_design import ReadableBuffer


Address: TypeAlias = tuple[Any, ...] | str | ReadableBuffer

ADDRESS_FAMILY_INET: Final[int]
SOCKET_STREAM: Final[int]

# ---- Classes ----

@disjoint_base
class Socket:
    # Close the connection
    def close(self) -> None: ...
    # Connect to a server
    def connect(self, address: Address, /) -> None: ...
    # Send data
    def sendall(self, data: ReadableBuffer, flags: int = 0, /) -> int: ...
    # Receive data
    def receive(self, buffer_size: int, flags: int = 0, /) -> bytes: ...

SocketType = Socket

# ---- Functions ----

# Close the connection
def close(file_descriptor: SupportsIndex, /) -> None: ...