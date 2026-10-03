#!/usr/bin/env python3
"""Legacy alias → scripts/verify_dup_suite.py (DUP Protocol dual-repo verify)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

target = Path(__file__).resolve().parent / "verify_dup_suite.py"
raise SystemExit(subprocess.call([sys.executable, str(target), *sys.argv[1:]]))
