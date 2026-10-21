#!/usr/bin/env python3
"""Install the bundled local Codex pet. Requires Python 3.9+, no packages."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import uuid


def install():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, help="Override CODEX_HOME / ~/.codex")
    parser.add_argument("--replace", action="store_true", help="Back up an existing peach-cat and replace it")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    source = root / "pets" / "peach-cat"
    checksums = {}
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        checksums[name] = digest
    for name in ("pet.json", "spritesheet.png"):
        relative = "pets/peach-cat/" + name
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != checksums[relative]:
            raise ValueError("Checksum mismatch: " + relative + "; download the package again.")
    manifest = json.loads((source / "pet.json").read_text(encoding="utf-8"))
    if manifest.get("id") != "peach-cat" or manifest.get("spritesheetPath") != "spritesheet.png":
        raise ValueError("Unexpected pet manifest")
    header = (source / "spritesheet.png").read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", header[16:24]) != (1536, 1872):
        raise ValueError("Expected a 1536x1872 PNG spritesheet")

    home = (args.codex_home or Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")).expanduser().resolve()
    parent = home / "pets"
    target = parent / "peach-cat"
    if target.is_symlink():
        raise ValueError("Refusing to replace a symbolic link: " + str(target))
    if target.exists() and not args.replace:
        raise ValueError("Pet already exists. Use --replace to back it up before installing.")
    parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".peach-cat-", dir=parent))
    backup = None
    try:
        for name in ("pet.json", "spritesheet.png"):
            shutil.copy2(source / name, stage / name)
        if target.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = home / "pet-backups" / ("peach-cat-" + stamp + "-" + uuid.uuid4().hex[:8])
            backup.parent.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
        try:
            stage.rename(target)
        except OSError:
            if backup is not None:
                backup.rename(target)
            raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    print("Installed peach-cat at: " + str(target))
    if backup is not None:
        print("Previous pet backed up at: " + str(backup))
    print("Refresh/restart your compatible Codex client and select 蜜桃猫 (peach-cat).")


if __name__ == "__main__":
    try:
        install()
    except (OSError, ValueError, KeyError, struct.error) as error:
        print("Installation failed: " + str(error), file=sys.stderr)
        sys.exit(1)
