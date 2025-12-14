# src/fyodoros/kernel/rootfs.py
"""
Virtual Root Filesystem.
"""

import os
from pathlib import Path

# 1. FYODOR_ROOT constant
FYODOR_ROOT = Path.home() / ".fyodor"
# Cache the resolved root path to avoid repeated syscalls
_RESOLVED_ROOT = None


class SecurityError(Exception):
    """Raised when a path traversal attempt is detected."""
    pass

def init_structure():
    """
    Creates the required directory structure on the disk.
    """
    directories = [
        FYODOR_ROOT / "bin",
        FYODOR_ROOT / "etc",
        FYODOR_ROOT / "home",
        FYODOR_ROOT / "var" / "logs",
        FYODOR_ROOT / "var" / "memory",
        FYODOR_ROOT / "sandbox",
        FYODOR_ROOT / "plugins",
    ]

    for d in directories:
        d.mkdir(parents=True, exist_ok=True)

def get_resolved_root() -> Path:
    """
    Returns the resolved absolute path of FYODOR_ROOT.
    Uses caching to avoid repeated filesystem calls.
    """
    global _RESOLVED_ROOT
    if _RESOLVED_ROOT is None:
        _RESOLVED_ROOT = FYODOR_ROOT.resolve()
    return _RESOLVED_ROOT


def resolve(virtual_path: str) -> Path:
    """
    Resolves a virtual path to a safe absolute path within FYODOR_ROOT.

    Args:
        virtual_path (str): The virtual path (e.g., "/home/notes.txt").

    Returns:
        Path: The absolute path on the host system.

    Raises:
        SecurityError: If the resolved path is outside FYODOR_ROOT.
    """
    # Normalize input: Ensure it looks like a relative path to join safely
    # If path starts with /, strictly speaking path.join with absolute path ignores previous part.
    # So we must strip leading /
    clean_path = virtual_path.lstrip("/")

    # Resolve absolute path
    target_path = (FYODOR_ROOT / clean_path).resolve()

    # Get cached root path
    root_abs = get_resolved_root()

    # Security Check: Ensure containment
    # Optimization: Use string prefix check instead of os.path.commonpath for performance.
    # commonpath is O(N) where N is number of path components, and involves string parsing.
    # startswith is O(L) where L is string length, which is much faster.
    root_str = str(root_abs)
    target_str = str(target_path)
    if not (target_str == root_str or target_str.startswith(os.path.join(root_str, ""))):
        raise SecurityError(f"Path traversal detected: {virtual_path} -> {target_path}")

    return target_path
