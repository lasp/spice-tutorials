"""Download and cache public SPICE kernels for the SPICE Book Club notebooks.

Kernels come from the NAIF server and are cached on local disk, so each file is
downloaded once. Works the same in Colab, Binder and a local checkout.

Typical use::

    from spiceclub import kernels
    lsk = kernels.fetch("generic_kernels/lsk/naif0012.tls")
    fk  = kernels.maven("fk")          # newest MAVEN frames kernel
    paths = kernels.generic()          # dict of the generic LSK, PCK and planet SPK

Where kernels are cached, first match wins:

1. the ``SPICECLUB_KERNELS`` environment variable;
2. the ``kernels/`` folder of a spice-tutorials checkout (found by walking up
   from the current directory);
3. ``~/spiceclub_kernels``.
"""

from __future__ import annotations

import os
import re
import shutil
import tempfile
import urllib.request
from pathlib import Path

#: NAIF's public kernel server; set SPICECLUB_NAIF_URL to use a mirror.
NAIF = os.environ.get("SPICECLUB_NAIF_URL", "https://naif.jpl.nasa.gov/pub/naif/").rstrip("/") + "/"
MAVEN_KERNELS = NAIF + "MAVEN/kernels/"

#: Generic kernels used from Session 1 on.
GENERIC = {
    "lsk": "generic_kernels/lsk/naif0012.tls",
    "pck": "generic_kernels/pck/pck00011.tpc",
    "spk": "generic_kernels/spk/planets/de440s.bsp",
}

#: MAVEN kernel families: (subdirectory, regex for the file name).
#: ``maven()`` picks the newest match, so the course survives NAIF version bumps.
MAVEN = {
    "fk": ("fk/", r"maven_v\d+\.tf"),
    "sclk": ("sclk/", r"MVN_SCLKSCET\.\d+\.tsc"),
}

_USER_AGENT = "spiceclub/0.1 (+https://github.com/lasp/spice-tutorials)"


def cache_dir() -> Path:
    """Return (and create) the directory where kernels are cached."""
    env = os.environ.get("SPICECLUB_KERNELS")
    if env:
        path = Path(env).expanduser()
    else:
        path = None
        for parent in [Path.cwd(), *Path.cwd().parents]:
            candidate = parent / "kernels"
            if (candidate / "README.md").is_file() and (parent / "_quarto.yml").is_file():
                path = candidate
                break
        if path is None:
            path = Path.home() / "spiceclub_kernels"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _url(path_or_url: str) -> str:
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    return NAIF + path_or_url.lstrip("/")


def fetch(path_or_url: str, force: bool = False, verbose: bool = True) -> Path:
    """Download one kernel into the cache (unless already there) and return its path.

    ``path_or_url`` is either a full URL or a path relative to the NAIF
    ``/pub/naif/`` directory, e.g. ``"generic_kernels/lsk/naif0012.tls"``.
    The download goes to a temporary file first and is checked against the
    server's Content-Length, so an interrupted transfer never leaves a
    truncated kernel in the cache.
    """
    url = _url(path_or_url)
    dest = cache_dir() / url.rsplit("/", 1)[-1]
    if dest.exists() and not force:
        return dest

    if verbose:
        print(f"Downloading {url}")
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        expected = resp.headers.get("Content-Length")
        with tempfile.NamedTemporaryFile(dir=dest.parent, delete=False) as tmp:
            shutil.copyfileobj(resp, tmp, length=1 << 20)
            tmp_path = Path(tmp.name)

    size = tmp_path.stat().st_size
    if expected is not None and size != int(expected):
        tmp_path.unlink(missing_ok=True)
        raise IOError(f"{url}: got {size} bytes, expected {expected}")
    tmp_path.replace(dest)
    if verbose:
        print(f"  saved {dest} ({size / 1e6:.1f} MB)")
    return dest


def listing(dir_url: str, pattern: str) -> list[str]:
    """Return file names in a NAIF directory listing that fully match ``pattern``, sorted."""
    req = urllib.request.Request(_url(dir_url), headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        html = resp.read().decode("utf-8", "replace")
    names = {m for m in re.findall(r'href="([^"/?]+)"', html) if re.fullmatch(pattern, m)}
    return sorted(names, key=_natural_key)


def _natural_key(name: str):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def latest(dir_url: str, pattern: str) -> str:
    """Full URL of the newest file (by version number) matching ``pattern``."""
    names = listing(dir_url, pattern)
    if not names:
        raise FileNotFoundError(f"no file matching {pattern!r} in {_url(dir_url)}")
    return _url(dir_url).rstrip("/") + "/" + names[-1]


def generic(force: bool = False) -> dict[str, Path]:
    """Fetch the generic LSK, PCK and planetary SPK; return ``{"lsk": Path, ...}``."""
    return {kind: fetch(path, force=force) for kind, path in GENERIC.items()}


def maven(kind: str, force: bool = False) -> Path:
    """Fetch the newest MAVEN kernel of ``kind`` (``"fk"`` or ``"sclk"``).

    If the cache already holds a matching file and ``force`` is False, the
    newest cached one is used without contacting NAIF.
    """
    subdir, pattern = MAVEN[kind]
    if not force:
        cached = sorted(
            (p.name for p in cache_dir().iterdir() if re.fullmatch(pattern, p.name)),
            key=_natural_key,
        )
        if cached:
            return cache_dir() / cached[-1]
    return fetch(latest(MAVEN_KERNELS + subdir, pattern), force=force)


def write_metakernel(path: str | os.PathLike, kernels: list[str | os.PathLike],
                     comment: str = "") -> Path:
    """Write a meta-kernel listing ``kernels`` and return its path.

    Paths are written as absolute paths using a ``$KERNELS`` path symbol, which
    keeps each string well under SPICE's 255-character limit and makes the file
    independent of the working directory it is loaded from.
    """
    kdir = cache_dir()
    entries = []
    for k in kernels:
        p = Path(k).resolve()
        try:
            entries.append("$KERNELS/" + p.relative_to(kdir.resolve()).as_posix())
        except ValueError:
            entries.append(p.as_posix())
    body = "\n".join(f"      '{e}'" for e in entries)
    text = (
        "KPL/MK\n\n"
        f"{comment or 'Meta-kernel written by spiceclub.kernels.write_metakernel.'}\n\n"
        "\\begindata\n\n"
        f"   PATH_VALUES  = ( '{kdir.resolve().as_posix()}' )\n"
        "   PATH_SYMBOLS = ( 'KERNELS' )\n\n"
        "   KERNELS_TO_LOAD = (\n"
        f"{body}\n"
        "   )\n\n"
        "\\begintext\n"
    )
    out = Path(path)
    out.write_text(text)
    return out
