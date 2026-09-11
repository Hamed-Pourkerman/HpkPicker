"""Install HPK Picker for detected Autodesk hosts.

Usage from a regular Windows Python prompt::

    python install.py
    python install.py --dry-run
    python install.py --hosts maya,3dsmax
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

APP_NAME = "HPKPicker_Upgrade_2026"
SUPPORTED_MAYA_MIN = 2022
SUPPORTED_MAX_MIN = 2024


def _versions_from_dirs(base: Path, prefix: str, minimum: int) -> list[int]:
    found = []
    if base.exists():
        for child in base.iterdir():
            if child.is_dir() and child.name.startswith(prefix):
                try:
                    version = int(child.name[len(prefix):].split(".", 1)[0])
                except ValueError:
                    continue
                if version >= minimum:
                    found.append(version)
    return sorted(set(found))


def detect_hosts() -> dict[str, list[int]]:
    """Detect supported installed versions without importing Autodesk APIs."""
    program_files = [Path(os.environ.get("ProgramFiles", r"C:\Program Files"))]
    local_app_data = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    maya_versions = set()
    max_versions = set()
    for root in program_files:
        maya_versions.update(_versions_from_dirs(root / "Autodesk", "Maya", SUPPORTED_MAYA_MIN))
        maya_versions.update(_versions_from_dirs(root / "Autodesk", "Maya ", SUPPORTED_MAYA_MIN))
        max_versions.update(_versions_from_dirs(root / "Autodesk", "3ds Max ", SUPPORTED_MAX_MIN))
    # Autodesk may be installed on another drive; registry lookup is best effort.
    try:
        import winreg
        for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            for key_name in (r"SOFTWARE\Autodesk\Maya", r"SOFTWARE\WOW6432Node\Autodesk\Maya"):
                try:
                    with winreg.OpenKey(hive, key_name) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            name = winreg.EnumKey(key, i)
                            if name.isdigit() and int(name) >= SUPPORTED_MAYA_MIN:
                                maya_versions.add(int(name))
                except OSError:
                    pass
    except ImportError:
        pass
    return {"maya": sorted(maya_versions), "3dsmax": sorted(max_versions)}


def _copy_package(destination: Path, source: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("hpkpicker", "resources"):
        target = destination / name
        shutil.copytree(source / name, target, dirs_exist_ok=True)


def _install_maya(source: Path, version: int, dry_run: bool) -> Path:
    destination = Path.home() / "Documents" / "maya" / str(version) / "scripts" / APP_NAME
    if not dry_run:
        _copy_package(destination, source)
        (destination / "HPKPicker_Maya_Shelf.py").write_text(
            f"import sys\nsys.path.insert(0, r'{destination}')\n"
            "from hpkpicker.maya_entry import run\nrun()\n", encoding="utf-8"
        )
    return destination


def _install_max(source: Path, version: int, dry_run: bool) -> Path:
    destination = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "Autodesk" / f"3dsMax\{version}" / "ENU" / "scripts" / APP_NAME
    if not dry_run:
        _copy_package(destination, source)
        launcher = destination / "HPKPicker_3dsMax.mcr"
        launcher.write_text(
            f'python.Execute "import sys; sys.path.insert(0, r\'{destination}\'); from hpkpicker.max_entry import run; run()"\n',
            encoding="utf-8",
        )
    return destination


def install(hosts: dict[str, list[int]], source: Path, dry_run: bool = False) -> list[Path]:
    installed = []
    for version in hosts.get("maya", []):
        installed.append(_install_maya(source, version, dry_run))
    for version in hosts.get("3dsmax", []):
        installed.append(_install_max(source, version, dry_run))
    return installed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="only show detected destinations")
    parser.add_argument("--hosts", help="comma-separated subset: maya,3dsmax")
    args = parser.parse_args(argv)
    detected = detect_hosts()
    if args.hosts:
        selected = {name.strip().lower() for name in args.hosts.split(",")}
        detected = {name: versions for name, versions in detected.items() if name in selected}
    print(f"Detected: {detected}")
    installed = install(detected, Path(__file__).resolve().parent, args.dry_run)
    for path in installed:
        print(f"{'Would install' if args.dry_run else 'Installed'}: {path}")
    if not installed:
        print("No supported Maya 2022+ or 3ds Max 2024+ installation was detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
