"""Deprecated.

Bulk lift has been retired. Use `tw.py fallback --id <id> --media-id <media-id> --role <role>
--confirm-origin-unavailable` after confirming the origin is unavailable.
"""
from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - deprecated entry
    del argv
    sys.stderr.write(
        "lift_catbox.py is retired; use tw.py fallback with --confirm-origin-unavailable\n"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
