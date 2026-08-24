"""Typed data model for the Twitter archive pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self
import json


@dataclass(frozen=True)
class PostMetrics:
    """Post engagement counters (replies / reposts / likes / views)."""
    reply_count: int
    repost_count: int
    like_count: int
    view_count: int | None


@dataclass(frozen=True)
class PostData:
    """A single tweet post extracted from a Twitter archive."""
    post_id: str
    author: str
    handle: str
    text: str
    timestamp: str
    media_urls: tuple[str, ...]
    reply_to_id: str | None
    quote_of_id: str | None
    metrics: PostMetrics


@dataclass(frozen=True)
class ThreadData:
    """A complete Twitter thread (root post + replies)."""
    root_post_id: str
    posts: tuple[PostData, ...]
    source_url: str


@dataclass(frozen=True)
class MediaLocationCheck:
    """Origin/fallback URL HEAD probe outcome stored on a location."""
    status: int | None
    result: str
    detail: str


@dataclass(frozen=True)
class MediaLocation:
    """A single media location record (local / origin / fallback / mirror / derived)."""
    kind: str
    id: str | None = None
    local_path: Path | None = None
    url: str | None = None
    bytes: int | None = None
    sha256: str | None = None
    media_type: str | None = None
    integrity: str | None = None
    verified_at: str | None = None
    provider: str | None = None
    availability: str | None = None
    checked_at: str | None = None
    checked_status: int | None = None
    recorded_at: str | None = None
    uploaded_at: str | None = None
    confirmed_unavailable_at: str | None = None
    check: MediaLocationCheck | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        if "kind" not in raw:
            raise KeyError("MediaLocation.from_dict: 'kind' is required")
        # Wire uses 'path' (basename) or 'local_path' (Path string) interchangeably
        path_raw = raw.get("local_path")
        if path_raw is None:
            path_raw = raw.get("path")
        check_raw = raw.get("check")
        check: MediaLocationCheck | None = None
        if check_raw is not None:
            if not isinstance(check_raw, dict):
                raise TypeError(
                    f"check: expected dict, got {type(check_raw).__name__}"
                )
            if "result" not in check_raw or "detail" not in check_raw:
                raise KeyError("MediaLocation.from_dict: 'check' requires 'result' and 'detail'")
            check = MediaLocationCheck(
                status=_optional_int(check_raw.get("status"), "check.status"),
                result=_required_str(check_raw.get("result"), "check.result"),
                detail=_required_str(check_raw.get("detail"), "check.detail"),
            )
        return cls(
            kind=_required_str(raw["kind"], "kind"),
            id=_optional_str(raw.get("id"), "id"),
            local_path=_optional_path(path_raw, "local_path"),
            url=_optional_str(raw.get("url"), "url"),
            bytes=_optional_int(raw.get("bytes"), "bytes"),
            sha256=_optional_str(raw.get("sha256"), "sha256"),
            media_type=_optional_str(raw.get("media_type"), "media_type"),
            integrity=_optional_str(raw.get("integrity"), "integrity"),
            verified_at=_optional_str(raw.get("verified_at"), "verified_at"),
            provider=_optional_str(raw.get("provider"), "provider"),
            availability=_optional_str(raw.get("availability"), "availability"),
            checked_at=_optional_str(raw.get("checked_at"), "checked_at"),
            checked_status=_optional_int(raw.get("checked_status"), "checked_status"),
            recorded_at=_optional_str(raw.get("recorded_at"), "recorded_at"),
            uploaded_at=_optional_str(raw.get("uploaded_at"), "uploaded_at"),
            confirmed_unavailable_at=_optional_str(
                raw.get("confirmed_unavailable_at"), "confirmed_unavailable_at"
            ),
            check=check,
        )


@dataclass(frozen=True)
class DerivedFromRef:
    """Pointer to the parent (orig) media item for derived items (crt, ocr, etc.)."""
    post_id: str
    media_id: str
    role: str


@dataclass(frozen=True)
class Publication:
    """Selected location for a media item; embedded as 'publication' on the wire."""
    selected_location_id: str
    selected_at: str
    reason: str


@dataclass(frozen=True)
class MediaItem:
    """A single media entry attached to a post (orig / crt / crt_outline / denoise / ocr).

    For legacy (pre-v2) wire shapes, ``locations`` may be empty and ``filename``
    plus ``url`` carry the original on-disk filename and pre-migration fallback
    URL. v2 items leave both ``None`` and put the URL inside a ``MediaLocation``.
    """
    post_id: str
    media_id: str
    locations: tuple[MediaLocation, ...] = ()
    kind: str | None = None
    handle: str | None = None
    role: str | None = None
    filename: str | None = None
    url: str | None = None
    embed: bool | None = None
    caption: str | None = None
    derived_from: DerivedFromRef | None = None
    publication: Publication | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        for required in ("post_id", "media_id"):
            if required not in raw:
                raise KeyError(f"MediaItem.from_dict: '{required}' is required")
        locations_raw = raw.get("locations")
        locations: tuple[MediaLocation, ...] = ()
        if locations_raw is not None:
            if not isinstance(locations_raw, list):
                raise TypeError(
                    f"MediaItem.from_dict: 'locations' must be list, got {type(locations_raw).__name__}"
                )
            locations = tuple(MediaLocation.from_dict(loc) for loc in locations_raw)
        # Wire uses 'role' as the kind identifier; accept 'kind' for direct callers
        kind_raw = raw.get("role")
        if kind_raw is None:
            kind_raw = raw.get("kind")
        if kind_raw is None:
            raise KeyError("MediaItem.from_dict: 'role' or 'kind' is required")
        kind = _required_str(kind_raw, "role")
        derived_from_raw = raw.get("derived_from")
        derived_from: DerivedFromRef | None = None
        if derived_from_raw is not None:
            if not isinstance(derived_from_raw, dict):
                raise TypeError(
                    f"derived_from: expected dict, got {type(derived_from_raw).__name__}"
                )
            derived_from = DerivedFromRef(
                post_id=_required_str(
                    derived_from_raw.get("post_id"), "derived_from.post_id"
                ),
                media_id=_required_str(
                    derived_from_raw.get("media_id"), "derived_from.media_id"
                ),
                role=_required_str(derived_from_raw.get("role"), "derived_from.role"),
            )
        publication_raw = raw.get("publication")
        publication: Publication | None = None
        if publication_raw is not None:
            if not isinstance(publication_raw, dict):
                raise TypeError(
                    f"publication: expected dict, got {type(publication_raw).__name__}"
                )
            publication = Publication(
                selected_location_id=_required_str(
                    publication_raw.get("selected_location_id"),
                    "publication.selected_location_id",
                ),
                selected_at=_required_str(
                    publication_raw.get("selected_at"), "publication.selected_at"
                ),
                reason=_required_str(publication_raw.get("reason"), "publication.reason"),
            )
        return cls(
            post_id=_required_str(raw["post_id"], "post_id"),
            media_id=_required_str(raw["media_id"], "media_id"),
            kind=kind,
            handle=_optional_str(raw.get("handle"), "handle"),
            role=_optional_str(raw.get("role"), "role"),
            filename=_optional_str(raw.get("filename"), "filename"),
            url=_optional_str(raw.get("url"), "url"),
            locations=locations,
            embed=_optional_bool(raw.get("embed"), "embed"),
            caption=_optional_str(raw.get("caption"), "caption"),
            derived_from=derived_from,
            publication=publication,
        )


@dataclass(frozen=True)
class MediaManifest:
    """A whole media.json document (one thread). schema_version is the wire key."""
    root_post_id: str
    items: tuple[MediaItem, ...]
    schema_version: int | None = None
    captured_at: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        for required in ("root_post_id", "items"):
            if required not in raw:
                raise KeyError(f"MediaManifest.from_dict: '{required}' is required")
        items_raw = raw["items"]
        if not isinstance(items_raw, list):
            raise TypeError(
                f"MediaManifest.from_dict: 'items' must be list, got {type(items_raw).__name__}"
            )
        return cls(
            root_post_id=_required_str(raw["root_post_id"], "root_post_id"),
            items=tuple(MediaItem.from_dict(item) for item in items_raw),
            schema_version=_optional_int(raw.get("schema_version"), "schema_version"),
            captured_at=_optional_str(raw.get("captured_at"), "captured_at"),
        )


@dataclass(frozen=True)
class LegacyThreadData:
    """Pre-v2 thread_data.json shape paired with media items during migration."""
    root_post_id: str
    posts: tuple[PostData, ...]
    source_url: str
    media_items: tuple[MediaItem, ...] = ()

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        for required in ("root_post_id", "posts", "source_url"):
            if required not in raw:
                raise KeyError(f"LegacyThreadData.from_dict: '{required}' is required")
        posts_raw = raw["posts"]
        if not isinstance(posts_raw, list):
            raise TypeError(
                f"LegacyThreadData.from_dict: 'posts' must be list, got {type(posts_raw).__name__}"
            )
        media_items_raw = raw.get("media_items")
        media_items: tuple[MediaItem, ...] = ()
        if media_items_raw is not None:
            if not isinstance(media_items_raw, list):
                raise TypeError(
                    f"LegacyThreadData.from_dict: 'media_items' must be list, got {type(media_items_raw).__name__}"
                )
            media_items = tuple(MediaItem.from_dict(item) for item in media_items_raw)
        return cls(
            root_post_id=_required_str(raw["root_post_id"], "root_post_id"),
            posts=tuple(_parse_post(p) for p in posts_raw),
            source_url=_required_str(raw["source_url"], "source_url"),
            media_items=media_items,
        )


@dataclass(frozen=True)
class LegacyManifest:
    """Pre-v2 corpus inventory shape used during media migration."""
    threads: tuple[LegacyThreadData, ...]
    schema_version: int | None = None
    generated_at: str | None = None
    counts: dict[str, int] | None = None
    frozen_hashes: dict[str, str] | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        if "threads" not in raw:
            raise KeyError("LegacyManifest.from_dict: 'threads' is required")
        threads_raw = raw["threads"]
        if not isinstance(threads_raw, list):
            raise TypeError(
                f"LegacyManifest.from_dict: 'threads' must be list, got {type(threads_raw).__name__}"
            )
        counts: dict[str, int] | None = _coerce_str_int_map(raw.get("counts"), "counts")
        frozen_hashes: dict[str, str] | None = _coerce_str_str_map(
            raw.get("frozen_hashes"), "frozen_hashes"
        )
        return cls(
            threads=tuple(LegacyThreadData.from_dict(t) for t in threads_raw),
            schema_version=_optional_int(raw.get("schema_version"), "schema_version"),
            generated_at=_optional_str(raw.get("generated_at"), "generated_at"),
            counts=counts,
            frozen_hashes=frozen_hashes,
        )


@dataclass(frozen=True)
class OriginCheck:
    """Outcome of a HEAD probe against a media item's origin URL.

    ``status`` is the HTTP status code returned by the probe (or ``None`` if
    the request errored before a response arrived). ``result`` is the
    classifier label (``"available"`` for 2xx/3xx, ``"error"`` otherwise).
    ``confirms_unavailable`` distinguishes transient failures like 429 from
    definitive unavailability so the caller does not flip the location's
    availability state on a rate-limit blip.
    """
    checked_at: str
    status: int | None
    result: str
    detail: str
    confirms_unavailable: bool


@dataclass(frozen=True)
class LegacyMediaJson:
    """Per-thread ``media.json`` shape consumed by ``media_migrate.py`` and ``media_audit.py``.

    Holds both the pre-v2 (legacy) and v2 (canonical) wire shapes so the
    migration and audit entry points can share one boundary type. The
    ``items`` field is parsed as ``MediaItem`` instances; for legacy items
    ``locations`` is empty and ``filename`` plus ``url`` carry the
    on-disk filename and pre-migration fallback URL.

    ``mirrors`` hold opaque destination/auth fields that are intentionally
    not yet typed. This is the only non-typed dict in the data model — it
    is consumed only by iteration, never by attribute access, and we
    deliberately do not commit to a structure until the backup subsystem
    settles on a wire shape.
    """
    schema_version: int | None
    root_post_id: str
    items: tuple[MediaItem, ...]
    captured_at: str | None
    mirrors: dict[str, Any] | None = None
    frozen: bool | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        if "root_post_id" not in raw:
            raise KeyError("LegacyMediaJson.from_dict: 'root_post_id' is required")
        items_raw = raw.get("items")
        if items_raw is None:
            items_raw = []
        if not isinstance(items_raw, list):
            raise TypeError(
                f"LegacyMediaJson.from_dict: 'items' must be list, got {type(items_raw).__name__}"
            )
        mirrors = _coerce_mirrors(raw.get("mirrors"), "mirrors")
        return cls(
            schema_version=_optional_int(raw.get("schema_version"), "schema_version"),
            root_post_id=_required_str(raw["root_post_id"], "root_post_id"),
            items=tuple(MediaItem.from_dict(item) for item in items_raw),
            captured_at=_optional_str(raw.get("captured_at"), "captured_at"),
            mirrors=mirrors,
            frozen=_optional_bool(raw.get("frozen"), "frozen"),
        )


def _coerce_str_int_map(value: object, field: str) -> dict[str, int] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError(f"{field}: expected dict, got {type(value).__name__}")
    out: dict[str, int] = {}
    for key, item in value.items():
        if isinstance(item, bool) or not isinstance(item, int):
            raise TypeError(f"{field}[{key}]: expected int")
        out[str(key)] = item
    return out


def _coerce_str_str_map(value: object, field: str) -> dict[str, str] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError(f"{field}: expected dict, got {type(value).__name__}")
    out: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(item, str):
            raise TypeError(f"{field}[{key}]: expected str")
        out[str(key)] = item
    return out


def _coerce_mirrors(value: object, field: str) -> dict[str, Any] | None:
    """Accept the legacy ``mirrors: list[dict]`` wire and coerce to the typed mirrors shape.

    Legacy producers (pre-LegacyMediaJson) wrote ``mirrors`` as a list of
    destination entries; current producers may write it as a dict keyed by
    destination id. Both shapes are accepted; the returned dict is keyed
    by ``destination_id`` when present on each entry, falling back to the
    string index for entries without one.
    """
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        coerced: dict = {}
        for index, entry in enumerate(value):
            if isinstance(entry, dict) and "destination_id" in entry:
                coerced[str(entry["destination_id"])] = entry
            else:
                coerced[str(index)] = entry
        return coerced
    raise TypeError(f"{field}: expected dict or list, got {type(value).__name__}")


def _norm_handle(raw: str) -> str:
    h = (raw or "").strip()
    return h[1:] if h.startswith("@") else h


def _norm_id(raw: object) -> str | None:
    if raw is None:
        return None
    s = str(raw).strip()
    return s or None


def _required_str(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name}: expected str, got {type(value).__name__}")
    return value


def _optional_str(value: object, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{field}: expected str, got {type(value).__name__}")
    return value


def _optional_int(value: object, field: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field}: expected int, got {type(value).__name__}")
    return value


def _optional_bool(value: object, field: str) -> bool | None:
    if value is None:
        return None
    if not isinstance(value, bool):
        raise TypeError(f"{field}: expected bool, got {type(value).__name__}")
    return value


def _optional_path(value: object, field: str) -> Path | None:
    if value is None:
        return None
    if isinstance(value, Path):
        return value
    if isinstance(value, str):
        return Path(value)
    raise TypeError(f"{field}: expected str or Path, got {type(value).__name__}")


def _parse_post(raw: object) -> PostData:
    if not isinstance(raw, dict):
        raise TypeError(f"post entry: expected dict, got {type(raw).__name__}")
    m = raw.get("metrics") or {}
    if not isinstance(m, dict):
        raise TypeError(f"post entry metrics: expected dict, got {type(m).__name__}")
    view = m.get("view_count")
    media_urls_raw = raw.get("media_urls") or []
    if not isinstance(media_urls_raw, list):
        raise TypeError(
            f"post entry media_urls: expected list, got {type(media_urls_raw).__name__}"
        )
    return PostData(
        post_id=str(raw.get("post_id") or ""),
        author=str(raw.get("author") or ""),
        handle=_norm_handle(str(raw.get("handle") or "")),
        text=str(raw.get("text") or ""),
        timestamp=str(raw.get("timestamp") or ""),
        media_urls=tuple(str(u) for u in media_urls_raw),
        reply_to_id=_norm_id(raw.get("reply_to_id")),
        quote_of_id=_norm_id(raw.get("quote_of_id")),
        metrics=PostMetrics(
            reply_count=int(m.get("reply_count") or 0),
            repost_count=int(m.get("repost_count") or 0),
            like_count=int(m.get("like_count") or 0),
            view_count=int(view) if view is not None else None,
        ),
    )


def load_thread(path: Path) -> ThreadData:
    data = json.loads(path.read_text(encoding="utf-8"))
    posts: list[PostData] = []
    for pd in data.get("posts", []):
        m = pd.get("metrics") or {}
        view = m.get("view_count")
        posts.append(PostData(
            post_id=str(pd.get("post_id") or ""),
            author=str(pd.get("author") or ""),
            handle=_norm_handle(str(pd.get("handle") or "")),
            text=str(pd.get("text") or ""),
            timestamp=str(pd.get("timestamp") or ""),
            media_urls=tuple(pd.get("media_urls") or []),
            reply_to_id=_norm_id(pd.get("reply_to_id")),
            quote_of_id=_norm_id(pd.get("quote_of_id")),
            metrics=PostMetrics(
                reply_count=int(m.get("reply_count") or 0),
                repost_count=int(m.get("repost_count") or 0),
                like_count=int(m.get("like_count") or 0),
                view_count=int(view) if view is not None else None,
            ),
        ))
    return ThreadData(
        root_post_id=str(data.get("root_post_id") or ""),
        posts=tuple(posts),
        source_url=str(data.get("source_url") or ""),
    )
