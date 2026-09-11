# HPK Picker Upgrade 2026

This is a new, separate implementation package. The legacy files under
`HPKPicker_Max` and `HPKPicker_Maya` are not modified.

## Supported hosts

- Autodesk Maya 2022 and later (Python 3, PySide2)
- Autodesk 3ds Max 2024 and later (Python 3, PySide2, `pymxs`)

## Install

Run `python install.py` from this directory. The installer detects installed
versions and installs per-user copies. Use `python install.py --dry-run` to
preview destinations, or `--hosts maya,3dsmax` to limit the targets.

After installation, run `HPKPicker_Maya_Shelf.py` from Maya's Script Editor or
run the generated `HPKPicker_3dsMax.mcr` from 3ds Max's MAXScript Editor and
place it on a shelf.

Picker JSON files remain compatible with the legacy format. Image paths are
resolved relative to the saved layout when possible; the bundled default image
is used for new tabs.
