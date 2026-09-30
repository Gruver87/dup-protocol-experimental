# -*- coding: utf-8 -*-
"""Shim → ``network.sync.legacy_test_sync_manager`` (Phase D quarantine)."""
from __future__ import annotations

import warnings

warnings.warn(
    "network.sync.sync_manager is legacy-test-only; "
    "import network.sync.legacy_test_sync_manager",
    DeprecationWarning,
    stacklevel=2,
)

from network.sync.legacy_test_sync_manager import *  # noqa: F401,F403
