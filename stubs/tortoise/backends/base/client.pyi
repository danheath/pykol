# Stubs for tortoise.backends.base.client (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Sequence

class Capabilities:
    dialect: Any = ...
    requires_limit: Any = ...
    safe_indexes: Any = ...
    def __init__(self, dialect: str, *, safe_indexes: bool=..., requires_limit: bool=...) -> None: ...
    def __setattr__(self, attr: Any, value: Any): ...

class BaseDBAsyncClient:
    query_class: Any = ...
    executor_class: Any = ...
    schema_generator: Any = ...
    capabilities: Any = ...
    log: Any = ...
    connection_name: Any = ...
    def __init__(self, connection_name: str, **kwargs: Any) -> None: ...
    async def create_connection(self, with_db: bool) -> None: ...
    async def close(self) -> None: ...
    async def db_create(self) -> None: ...
    async def db_delete(self) -> None: ...
    def acquire_connection(self) -> ConnectionWrapper: ...
    async def execute_insert(self, query: str, values: list) -> int: ...
    async def execute_query(self, query: str) -> Sequence[dict]: ...
    async def execute_script(self, query: str) -> None: ...

class ConnectionWrapper:
    connection: Any = ...
    lock: Any = ...
    def __init__(self, connection: Any, lock: Any) -> None: ...
    async def __aenter__(self): ...
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...

class BaseTransactionWrapper:
    async def start(self) -> None: ...
    async def rollback(self) -> None: ...
    async def commit(self) -> None: ...
    async def __aenter__(self): ...
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
