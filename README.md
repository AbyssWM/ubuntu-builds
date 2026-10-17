# Abyss Ubuntu builds

Experimental Ubuntu source-package definitions for all 17 Abyss repositories.
Native clean-room builds, lintian checks and installation tests are **not yet
validated**. These are independent definitions, not packages in Ubuntu's archive.

`packages/NAME/debian/` holds the native packaging. `sources.json` pins upstream
commits and archive hashes. Dependency names share the Debian packaging basis;
Ubuntu versions and availability still require verification against the selected
Ubuntu series. Do not assume a successful Debian build also works on Ubuntu.

```sh
python3 tools/prepare-source.py abyssutils --out out/abyssutils
```

This verifies and assembles the source tree and deterministic orig archive.
It does not run a native build, sign an upload or create a PPA. Changelogs use
`UNRELEASED` until the target Ubuntu series has been explicitly selected and
its dependencies verified. The development archive currently points to 27.04;
that fact is not a commitment to target it or a claim of Mint compatibility.

The intended Launchpad account is `bb8therobot`; the PPA `abyss` still needs to
be created and an upload signing key configured by its owner. Build dependencies
in the order listed in `sources.json` before submitting dependants. No Launchpad
credentials or private signing keys belong in this Git repository.

Ubuntu-based Mint must be tested against its matching Ubuntu base; LMDE uses the
separate Debian packaging. A PPA does not automatically become enabled on Mint.

Maintainer: bb8TheRobot <bb8therobot85@gmail.com>. Packaging: 0BSD.
Original source notices and licenses remain applicable. Source attribution and
packaging-policy review remain release prerequisites.

License scope and the retained upstream notices are described in [LICENSES.md](LICENSES.md).
