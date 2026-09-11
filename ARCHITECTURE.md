# Refactor notes

The four supplied entry points were reviewed before creating this project.

The original Max launcher imports Qt and host modules globally, contains a
deprecated `MaxPlus` fallback, and uses a fixed repository path. The Maya
viewer combines nearly 3,000 lines of drawing, file I/O, dialog, and DCC
operations in one module. Both viewers duplicate selection/script logic and
use broad exception handlers, mutable class-level host flags, and Windows-only
path concatenation. The original shelf script also assumes `sys` was already
imported and hard-codes a machine-specific path.

The upgrade keeps the existing JSON layout schema and UI interactions while
making the host boundary explicit:

* `hpkpicker/viewer.py` contains the shared Qt editor.
* `hpkpicker/hosts/maya.py` owns `maya.cmds`, `OpenMayaUI`, and `shiboken2`.
* `hpkpicker/hosts/max.py` owns `pymxs` and `qtmax`.
* `hpkpicker/hosts/base.py` provides a safe offline adapter for parsing,
  packaging, and installer smoke tests.
* `install.py` discovers supported versions, installs per-user, and is safe to
  rerun without deleting an existing install directory.

No file in the legacy directories is changed by this project.
