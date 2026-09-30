# -*- coding: utf-8 -*-
"""Shim → ``network.sync.legacy_test_fast_sync`` (Phase D quarantine)."""
from __future__ import annotations

import warnings

warnings.warn(
    "network.sync.fast_sync is legacy-test-only; "
    "import network.sync.legacy_test_fast_sync",
    DeprecationWarning,
    stacklevel=2,
)

from network.sync.legacy_test_fast_sync import *  # noqa: F401,F403
