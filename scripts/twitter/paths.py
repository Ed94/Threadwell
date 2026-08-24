"""Repo-relative locations. Script lives at <vault>/scripts/twitter/."""
from __future__ import annotations

from pathlib import Path

HERE: Path = Path(__file__).resolve().parent
VAULT: Path = HERE.parent.parent
PROJECTS: Path = VAULT.parent
DUMPS: Path = PROJECTS / "manual_slop" / "docs" / "twitter"
WORKSPACE: Path = PROJECTS / "Threadwell-ai"
SCRATCH: Path = WORKSPACE / "scratch"
COOKIES: Path = VAULT / "secrets" / "twitter_cookies.txt"
FROZEN: Path = HERE / "do_not_refetch.txt"
