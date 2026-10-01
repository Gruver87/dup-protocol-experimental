"""HTTP + JSON-RPC client for DUP Protocol experimental nodes."""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from typing import Any, Dict, Mapping, MutableMapping, Optional, Union
from urllib.parse import urljoin, urlencode

from .amount import (
    from_satoshi_float,
    require_satoshi,
    to_satoshi,
    wei_hex_to_satoshi,
)
from .errors import HttpError, MoneyRefuse, RpcError
from .types import BalanceInfo, JsonDict, ReceiptInfo, TxSubmitResult


class Client:
    """Thin operator client (TLS verify on; satoshi-honest money).

    Parameters
    ----------
    base_url:
        Node HTTP base, e.g. ``http://127.0.0.1:18180`` (REST + JSON-RPC share host;
        JSON-RPC uses ``rpc_path``, default ``/``).
    api_key:
        Optional ``X-API-Key`` for RPC/REST auth.
    timeout:
        Socket timeout seconds.
    verify_tls:
        Must stay True. Passing False raises ``ValueError`` (fail-closed).
    rpc_path:
        JSON-RPC endpoint path (default ``/``).
    """

    def __init__(
        self,
        base_url: str,
        *,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        verify_tls: bool = True,
        rpc_path: str = "/",
    ) -> None:
        if verify_tls is not True:
            raise ValueError(
                "verify_tls=False is refused (dup_sdk fail-closed; no insecure TLS)"
            )
        self.base_url = (base_url or "").rstrip("/") + "/"
        self.api_key = (api_key or "").strip() or None
        self.timeout = float(timeout)
        self.rpc_path = rpc_path if rpc_path.startswith("/") else f"/{rpc_path}"
        self._ssl_ctx = ssl.create_default_context()
        self._rpc_id = 0

    # ── transport ─────────────────────────────────────────────────────────

    def _headers(self, *, content_type: Optional[str] = None) -> Dict[str, str]:
        headers: Dict[str, str] = {"Accept": "application/json"}
        if content_type:
            headers["Content-Type"] = content_type
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def _url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return urljoin(self.base_url, path.lstrip("/"))

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Union[Mapping[str, Any], list]] = None,
        query: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        url = self._url(path)
        if query:
            qs = urlencode({k: str(v) for k, v in query.items() if v is not None})
            url = f"{url}?{qs}" if "?" not in url else f"{url}&{qs}"
        data: Optional[bytes] = None
        headers = self._headers(
            content_type="application/json" if body is not None else None
        )
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(
                req, timeout=self.timeout, context=self._ssl_ctx
            ) as resp:
                raw = resp.read()
                if not raw:
                    return None
                try:
                    return json.loads(raw.decode("utf-8"))
                except json.JSONDecodeError as exc:
                    raise HttpError(
                        getattr(resp, "status", 200),
                        f"invalid JSON: {exc}",
                        path=path,
                    ) from exc
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", errors="replace")
            except Exception:
                detail = str(exc.reason)
            raise HttpError(int(exc.code), detail or str(exc.reason), path=path) from exc
        except urllib.error.URLError as exc:
            raise HttpError(0, str(exc.reason), path=path) from exc

    def get(self, path: str, *, query: Optional[Mapping[str, Any]] = None) -> Any:
        return self._request("GET", path, query=query)

    def post(self, path: str, body: Mapping[str, Any]) -> Any:
        return self._request("POST", path, body=dict(body))

    def rpc(self, method: str, params: Optional[list] = None) -> Any:
        self._rpc_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._rpc_id,
            "method": method,
            "params": list(params or []),
        }
        result = self._request("POST", self.rpc_path, body=payload)
        if not isinstance(result, dict):
            raise RpcError(-32603, "invalid RPC response envelope")
        if "error" in result and result["error"] is not None:
            err = result["error"]
            if isinstance(err, dict):
                raise RpcError(
                    int(err.get("code", -32000)),
                    str(err.get("message", "rpc error")),
                    data=err.get("data"),
                )
            raise RpcError(-32000, str(err))
        return result.get("result")

    # ── health / status ───────────────────────────────────────────────────

    def health_live(self) -> JsonDict:
        out = self.get("/health/live")
        return out if isinstance(out, dict) else {"raw": out}

    def health_ready(self) -> JsonDict:
        out = self.get("/health/ready")
        return out if isinstance(out, dict) else {"raw": out}

    def status(self) -> JsonDict:
        out = self.get("/status")
        return out if isinstance(out, dict) else {"raw": out}

    def status_probe(self) -> JsonDict:
        out = self.get("/status", query={"probe": "1"})
        return out if isinstance(out, dict) else {"raw": out}

    # ── chain / money ─────────────────────────────────────────────────────

    def get_block_number(self) -> int:
        raw = self.rpc("eth_blockNumber")
        if isinstance(raw, str):
            return int(raw, 16)
        return int(raw)

    def get_balance_satoshi(self, address: str) -> int:
        """Prefer REST ``/wallet/balance/{addr}``; fall back to eth_getBalance wei→sat."""
        addr = (address or "").strip()
        if not addr:
            raise MoneyRefuse("address required")
        try:
            out = self.get(f"/wallet/balance/{addr}")
            if isinstance(out, dict) and out.get("balance_satoshi") is not None:
                return require_satoshi(
                    satoshi=out["balance_satoshi"], field="balance"
                )
        except HttpError:
            pass
        wei_hex = self.rpc("eth_getBalance", [addr, "latest"])
        return wei_hex_to_satoshi(str(wei_hex))

    def get_balance(self, address: str) -> BalanceInfo:
        sat = self.get_balance_satoshi(address)
        info: BalanceInfo = {
            "address": address.strip(),
            "balance_satoshi": sat,
            "balance": from_satoshi_float(sat),
            "symbol": "ABS",
        }
        return info

    def get_tx_receipt(self, tx_hash: str) -> ReceiptInfo:
        h = (tx_hash or "").strip()
        if not h:
            raise ValueError("tx_hash required")
        try:
            out = self.get(f"/tx/receipt/{h}")
            if isinstance(out, dict):
                return self._normalize_receipt(out)
        except HttpError as exc:
            if exc.status != 404:
                # try eth path below; re-raise non-404 after fallback fail
                pass
            elif exc.status == 404:
                pass
        # eth_getTransactionReceipt fallback
        eth = self.rpc("eth_getTransactionReceipt", [h])
        if eth is None:
            raise HttpError(404, "receipt not found", path=f"/tx/receipt/{h}")
        if isinstance(eth, dict):
            return self._normalize_receipt(eth)
        raise HttpError(502, "unexpected receipt shape", path="eth_getTransactionReceipt")

    @staticmethod
    def _normalize_receipt(row: Mapping[str, Any]) -> ReceiptInfo:
        out: ReceiptInfo = {}
        if "tx_hash" in row:
            out["tx_hash"] = str(row["tx_hash"])
        elif "transactionHash" in row:
            out["tx_hash"] = str(row["transactionHash"])
        if "block_height" in row:
            out["block_height"] = int(row["block_height"] or 0)
        elif "blockNumber" in row and row["blockNumber"] is not None:
            bn = row["blockNumber"]
            out["block_height"] = int(bn, 16) if isinstance(bn, str) else int(bn)
        if "status" in row and row["status"] is not None:
            st = row["status"]
            if isinstance(st, str) and st.startswith("0x"):
                out["status"] = int(st, 16)
            else:
                out["status"] = int(st)
        for sat_key in ("value_satoshi", "fee_satoshi", "burned_satoshi"):
            if row.get(sat_key) is not None:
                out[sat_key] = int(row[sat_key])  # type: ignore[literal-required]
        for abs_key in ("value", "fee", "burned"):
            if abs_key in row and row[abs_key] is not None:
                try:
                    out[abs_key] = float(row[abs_key])  # type: ignore[literal-required]
                except (TypeError, ValueError):
                    pass
                sat_key = f"{abs_key}_satoshi"
                if sat_key not in out:
                    try:
                        out[sat_key] = to_satoshi(row[abs_key])  # type: ignore[literal-required]
                    except MoneyRefuse:
                        pass
        return out

    def submit_signed_tx(
        self,
        tx: Optional[Mapping[str, Any]] = None,
        *,
        raw_tx_hex: Optional[str] = None,
    ) -> TxSubmitResult:
        """Submit a pre-signed transaction.

        Prefer ``raw_tx_hex`` → ``eth_sendRawTransaction``.
        Otherwise POST ``/transactions`` with a signed body. Money fields must
        include integer ``amount_satoshi`` / ``fee_satoshi`` (or whole ABS ints);
        non-integral float-only money is refused client-side.
        """
        if raw_tx_hex:
            raw = raw_tx_hex.strip()
            if not raw.startswith("0x"):
                raw = "0x" + raw
            tx_hash = self.rpc("eth_sendRawTransaction", [raw])
            return {
                "tx_hash": str(tx_hash),
                "status": "pending",
                "trace_url": f"/tx/trace/{tx_hash}",
            }

        if not tx:
            raise ValueError("tx dict or raw_tx_hex required")

        body: MutableMapping[str, Any] = dict(tx)
        # Normalize money — refuse float-only dust
        amount_sat = None
        if body.get("amount_satoshi") is not None or body.get("value_satoshi") is not None:
            amount_sat = require_satoshi(
                satoshi=body.get("amount_satoshi", body.get("value_satoshi")),
                field="amount",
            )
        elif body.get("amount") is not None or body.get("value") is not None:
            amount_sat = require_satoshi(
                abs_amount=body.get("amount", body.get("value")),
                field="amount",
            )
        if amount_sat is not None:
            body["amount_satoshi"] = amount_sat
            body["value_satoshi"] = amount_sat
            body["amount"] = from_satoshi_float(amount_sat)
            body["value"] = body["amount"]

        if body.get("fee_satoshi") is not None or body.get("fee") is not None:
            fee_sat = require_satoshi(
                satoshi=body.get("fee_satoshi"),
                abs_amount=body.get("fee") if body.get("fee_satoshi") is None else None,
                field="fee",
            )
            body["fee_satoshi"] = fee_sat
            body["fee"] = from_satoshi_float(fee_sat)

        out = self.post("/transactions", body)
        if not isinstance(out, dict):
            raise HttpError(502, "unexpected submit response", path="/transactions")
        result: TxSubmitResult = {
            "tx_hash": str(out.get("tx_hash", "")),
            "status": str(out.get("status", "pending")),
        }
        if out.get("trace_url"):
            result["trace_url"] = str(out["trace_url"])
        return result
