"""Typed errors for dup_sdk (fail-closed)."""

from __future__ import annotations


class DupSdkError(Exception):
    """Base SDK error."""


class MoneyRefuse(DupSdkError, ValueError):
    """Float-only or invalid money input refused."""


class HttpError(DupSdkError):
    """Non-success HTTP response from the node."""

    def __init__(self, status: int, message: str, *, path: str = "") -> None:
        self.status = int(status)
        self.path = path
        super().__init__(f"HTTP {self.status} {path}: {message}")


class RpcError(DupSdkError):
    """JSON-RPC error object from the node."""

    def __init__(self, code: int, message: str, *, data: object = None) -> None:
        self.code = int(code)
        self.data = data
        super().__init__(f"RPC {self.code}: {message}")
