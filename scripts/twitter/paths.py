"""Repo-relative locations. Script lives at <vault>/scripts/twitter/."""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE.parent.parent
PROJECTS = VAULT.parent
DUMPS = PROJECTS / "manual_slop" / "docs" / "twitter"
WORKSPACE = PROJECTS / "Threadwell-ai"
SCRATCH = WORKSPACE / "scratch"
COOKIES = VAULT / "secrets" / "twitter_cookies.txt"
FROZEN = HERE / "do_not_refetch.txt"
