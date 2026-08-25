"""Test helpers for the Twitter full-conversation fetcher.

Owns the canonical test-truth constants that production
``twitter.fetch_thread`` mirrors (the equality is asserted at
import time once production exists). Also owns the offline fakes
used by every test that exercises the fetcher without touching
the network: ``FakeTransport``, ``RecordingSleeper``, and
``FakeTransaction``.

This module deliberately stays a *test-only* module: it must not
import ``twitter.fetch_thread`` (production does not exist yet
when the helpers are first created) and must not read cookies,
open sockets, or sleep for real.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

# --- canonical test-truth constants (production mirrors these) ---


KNOWN_ROOT_ID: str = "1650678968255913985"
KNOWN_TIP_ID: str = "1651282559287042048"

EXPECTED_16: frozenset[str] = frozenset({
    "1650678968255913985",  # kenpex OP
    "1650685805776732160",  # abductee_org -> OP
    "1650915682136240129",  # streleav -> OP
    "1651056827839180800",  # wadetb -> OP
    "1651086935467917312",  # ChristerEricson -> OP
    "1651168030557077504",  # SebAaltonen -> OP
    "1651253961524142081",  # kenpex -> wadetb
    "1651254727160795137",  # kenpex -> ChristerEricson
    "1651268028795961344",  # NOTimothyLottes -> kenpex
    "1651282559287042048",  # wvo (the input tip)
    "1651295755293036544",  # ErikHaliewicz -> OP
    "1651508233243095043",  # npatsiouras -> kenpex Christer branch
    "1651510424649744385",  # ChristerEricson -> npatsiouras
    "1651511316010663936",  # ChristerEricson -> self
    "1651579576089300992",  # JaceCear -> OP
    "1651636988267888641",  # kenpex -> JaceCear
})

# --- fixture loader ---


FIXTURES_DIR: Path = (
    Path(__file__).resolve().parent / "fixtures" / "fetch_thread"
)


def load_fixture(name: str) -> str:
    """Return the raw UTF-8 text of a sanitized fixture by basename.

    The caller may pass ``"tip_tweet_detail"`` or
    ``"tip_tweet_detail.json"``; either form resolves to the same
    file under :data:`FIXTURES_DIR`.
    """
    filename = name if name.endswith(".json") else f"{name}.json"
    return (FIXTURES_DIR / filename).read_text(encoding="utf-8")


def load_json_fixture(name: str) -> object:
    """Parse the JSON fixture with ``name`` (with or without the
    ``.json`` suffix) and return the deserialised value.

    Return type is ``object`` because the wire shape varies: pages,
    cursor lists, error envelopes, and homepage HTML fragments all
    round-trip through here.
    """
    return json.loads(load_fixture(name))


# --- fakes ---


@dataclass
class RecordingSleeper:
    """Records each requested sleep duration without blocking.

    The fetcher's :class:`RequestGovernor` calls ``sleep(min_delay)``
    after the first request of every role; tests assert the exact
    sequence and value via ``self.durations``.
    """

    durations: list[float] = field(default_factory=list)

    def sleep(self, seconds: float) -> None:
        """Append the requested duration; return immediately."""
        self.durations.append(seconds)


@dataclass
class FakeTransport:
    """In-memory transport. Issues no HTTP requests.

    The fetcher's production transport implements
    ``fetch(role, url) -> (status, body)``. The fake mirrors that
    signature so production and tests agree on the call surface.

    Attributes:
        responses: Role-keyed canned responses. Each value is a
            ``(status_code, body_text)`` pair. Missing keys raise
            ``AssertionError`` so tests fail loudly when a new role
            is introduced without a corresponding fixture.
        calls: Per-``fetch`` call record. Each entry is a dict with
            ``"role"`` and ``"url"`` keys, in call order.
    """

    responses: dict[str, tuple[int, str]] = field(default_factory=dict)
    calls: list[dict[str, str]] = field(default_factory=list)
    _transaction: object | None = None

    def set_transaction(self, transaction: object) -> None:
        """Store a fake transaction for later inspection.

        The real ``RequestsSessionTransport`` calls this once the
        two bootstrap requests succeed. Tests pass a
        :class:`FakeTransaction` (or any object) and assert the
        order by reading ``self._transaction`` later.
        """
        self._transaction = transaction

    def fetch(self, role: str, url: str) -> tuple[int, str]:
        """Return the canned response for ``role`` and record the call.

        Raises ``AssertionError`` if ``role`` is not keyed in
        :attr:`responses`; this is the offline equivalent of a 5xx
        when the live provider returns nothing for an unknown role.
        """
        if role not in self.responses:
            raise AssertionError(
                f"FakeTransport: no response registered for role {role!r}"
            )
        self.calls.append({"role": role, "url": url})
        return self.responses[role]


class FakeTransaction:
    """Fake MIT ``XClientTransaction``-shaped object for tests.

    The real constructor signature (verified offline) is
    ``ClientTransaction(home_page_response, ondemand_file_response,
    random_keyword=None, random_number=None)``. Tests capture both
    arguments verbatim so they can assert the fetcher passed the
    parsed ``BeautifulSoup`` and raw JS body to the factory in the
    right order. The ``generate_transaction_id`` method is directly
    defined on this class (delegating to the module-level
    :func:`generate_transaction_id` helper) so the fake exactly
    matches the real call surface.
    """

    def __init__(
        self,
        home_soup: object,
        js_body: object,
        **kwargs: object,
    ) -> None:
        self.home_soup = home_soup
        self.js_body = js_body
        self.kwargs = kwargs

    def generate_transaction_id(
        self,
        method: str,
        path: str,
        **kwargs: object,
    ) -> str:
        """Return a fixed test transaction id."""
        return generate_transaction_id(method, path, **kwargs)


_FIXED_TRANSACTION_ID: str = "fixed-test-transaction-id"


def generate_transaction_id(
    method: str,
    path: str,
    **kwargs: object,
) -> str:
    """Return a fixed transaction id for offline tests.

    The id value is irrelevant to behaviour; tests assert that the
    production code calls ``generate_transaction_id(method, path,
    **kwargs)`` and that the result reaches the request header.
    """
    return _FIXED_TRANSACTION_ID


def make_fake_transaction(
    home_soup: object,
    js_body: object,
    **kwargs: object,
) -> FakeTransaction:
    """Construct a :class:`FakeTransaction` with the production
    call signature so a test's ``transaction_factory`` matches the
    real ``ClientTransaction(home_page_response, ondemand_file_response)``
    two-positional-arg constructor.

    Exposed as a free function (rather than baking the signature
    into ``FakeTransaction``) so tests can pass it as a
    ``transaction_factory`` callable to the fetcher.
    """
    return FakeTransaction(home_soup, js_body, **kwargs)
