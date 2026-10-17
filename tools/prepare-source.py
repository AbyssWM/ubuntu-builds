#!/usr/bin/env python3
"""Verify pinned archives and assemble a Debian source tree and orig tarball."""

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import urllib.request

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("package")
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--cache", type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
sources = json.loads((root / "sources.json").read_text())
catalog = json.loads((root / "catalog.json").read_text())
source = next((p for p in sources["packages"] if catalog["packages"][p["repo"]]["name"] == args.package), None)
if source is None:
    parser.error("unknown package")
version = source["version"] + "+git" + sources["snapshot_date"] + "." + source["commit"][:7]
out = args.out.resolve()
out.mkdir(parents=True, exist_ok=True)
tree = out / (args.package + "-" + version)
if tree.exists():
    parser.error(f"source tree already exists: {tree}; use a fresh output directory")
cache = args.cache or out / "distfiles"
cache.mkdir(parents=True, exist_ok=True)


def verified(item):
    path = cache / item["filename"]
    if not path.is_file():
        with urllib.request.urlopen(item["url"], timeout=120) as response, path.open("wb") as output:
            shutil.copyfileobj(response, output)
    if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
        raise SystemExit(f"checksum mismatch: {path.name}")
    return path


staging = out / (args.package + "-extract")
staging.mkdir()
with tarfile.open(verified(source)) as archive:
    archive.extractall(staging, filter="data")
staging.joinpath(source["repo"] + "-" + source["commit"]).rename(tree)
if args.package == "abyssland":
    dep = tree / ".deps"
    dep.mkdir()
    with tarfile.open(verified(sources["extras"]["glaze"])) as archive:
        archive.extractall(dep, filter="data")
epoch = int(datetime.strptime(sources["snapshot_date"], "%Y%m%d").replace(tzinfo=timezone.utc).timestamp())


def normalize(info):
    info.uid = info.gid = 0
    info.uname = info.gname = "root"
    info.mtime = epoch
    return info


orig = out / f"{args.package}_{version}.orig.tar.gz"
with orig.open("wb") as output, gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as compressed:
    with tarfile.open(fileobj=compressed, mode="w") as archive:
        archive.add(tree, arcname=tree.name, filter=normalize)
shutil.copytree(root / "packages" / args.package / "debian", tree / "debian")
print(tree)
print(f"orig SHA256 {hashlib.sha256(orig.read_bytes()).hexdigest()}")
print("Next: select a target distribution in debian/changelog, then use native dpkg-buildpackage/sbuild.")
