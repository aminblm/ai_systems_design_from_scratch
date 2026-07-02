
# 44. CLI arguments parsers between modules

# 45. asyncio is too good to be true, coroutines, tasks, event loops

# 46. Async mixin design

# 47. How Asyncio solved my socket issue on not exiting on SystemExit

# 48. ASGI Servers

# 49. Await method

# 50. when looking up a codebase to learn from, look up the test suitecase where you can see actual data and usecases to relate to

# 51. I analysed the starlette codebase and found:

highly typed, highly async, stress tested, callables everywhere, fine grained datatypes, no bloit code, in pure python, usage of state, scope, class functions, custom types relating 
their business logic mostly MutableMapping, Callable, Awaitable, single responsibility modules, almost no docstrings except for their main application class and it is still very short,
least lines of code, a lot of class attriutes, no abstract classes, focus on HTTP and WebSockets endpoints and logic around them, main app is the Router that have all the routes,
still reliance on external libraries, basically passing everything in the constructors and exporting them via @property, usage of collections.abc, usage of Decorator, Strategy, Orchestrator, Factory, Singleton, SOLID,
Among other patterns, a well written test-suite covering many cases, non reliance on socket nor asyncio stdlib builtin, built their own sockets, 

# 52. P = ParamSpec("P") T = TypeVar("T")

# 53. Difference between collections.abs and typing

# 54. from contextlib import AbstractAsyncContextManager

# 55. typing Protocol

# 56. from typing_extensions import disjoint_base, TypeAlias

(function) def disjoint_base(cls: _TC@disjoint_base) -> _TC@disjoint_base

This decorator marks a class as a disjoint base.

Child classes of a disjoint base 
    cannot inherit from other disjoint bases 
        that are not parent classes of the disjoint base.

Child class cannot inherit from 2 or more disjoint bases
it creates a 1:1 mapping with the inheriting child class
of a sort

For example:

 @disjoint_base 
 class Disjoint1: pass 
 
 @disjoint_base 
 class Disjoint2: pass 
 
 class Disjoint3(Disjoint1, Disjoint2): pass # Type checker error

Type checkers can use knowledge of disjoint bases to detect unreachable code
and determine when two types can overlap.

See PEP 800.

# 57. Skill building: 1. understanding, 2. collecting, 3. executing from first Principles

# 58. Low level sockets understanding

# 59. the / and ... in a Python Function: def connect(self, address: Address, /) -> None: ...

# 60. from _typeshed import ReadableBuffer

ReadableBuffer seems to be accepting bytes

# 61. typing SupportsIndex

### 🔍 **Understanding `fd` in the Function Definition**

In the function definition:

```python
def close(fd: SupportsIndex, /) -> None:
```

- **`fd`**: This is the **file descriptor** (an integer) passed to the function. In the context of the `socket` module, `fd` refers to the **file descriptor** of a socket connection. When you call `socket.close()`, the `fd` parameter is the integer that identifies the socket.

- **`SupportsIndex`**: This is a **type annotation** (a Python type hint). In this case, it is a **type alias** for `int`. The `SupportsIndex` is a placeholder to indicate that the `fd` is an **integer**. In Python, this is redundant because `int` is a built-in type, but the annotation is used to clarify the expected type.

---

### 🧠 **What Does `fd` Represent?**

- **File Descriptor (FD)**: In Unix-like systems, a file descriptor is an integer that identifies an open file or socket. For example, when you create a socket with `socket.socket()`, the returned object has a `fileno()` method that returns its file descriptor.

- **In Python's `socket` Module**: The `close()` method of a socket object takes the file descriptor as an argument. This allows you to close the connection using the same syntax as the system-level `close()` function.

---

### 🧩 **Function Purpose**

The `close()` method is used to **terminate a socket connection**. It takes the file descriptor of the socket and closes it, releasing system resources.

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8080))
sock.close()  # fd is the file descriptor of the socket
```

---

### ✅ **Long-Term Value**

Understanding `fd` and its role in the `socket` module is critical for:

- **Network Programming**: You'll work with low-level socket operations, and `fd` is a fundamental concept.
- **Error Handling**: You'll learn to manage file descriptors correctly to avoid resource leaks.
- **Code Readability**: Type hints like `SupportsIndex` help you understand the expected input and output of functions.

---

### 📝 **Summary**

- **`fd`**: The file descriptor (integer) of the socket connection.
- **`SupportsIndex`**: A type hint indicating the parameter is an integer.
- **Function Purpose**: Close a socket connection using its file descriptor.

This understanding is foundational for working with network programming in Python and is essential for building robust, efficient applications.

# 62. Code with this principle in mind: If I will remove this code in future updates: Do not write it

Always ask yourself, will I be removing this code from future updates?
Always follow community and established principles from the beginning

# 63. Always be prioritizing Python primitives over typing ones (i.e. dict over Dict)

# 64. Always code with minimal code that gets the job done robustly

# 65. Avoid excessive loggin and tie it to a verbose state

# 66. Enforce Abstractions and encapsulations everywhere and let the clients consume the module components through the module interface only

# 67. that's a common pattern across the stdlib, the standard module foo is Python written, and core of it will be in _foo, which is a native module
