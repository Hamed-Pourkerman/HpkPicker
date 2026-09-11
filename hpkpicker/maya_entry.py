"""Maya shelf entry point."""

import importlib

from . import viewer


_dialog = None


def run():
    global _dialog
    if _dialog is not None:
        try:
            _dialog.close()
            _dialog.deleteLater()
        except RuntimeError:
            pass
    _dialog = viewer.PickerUI(parent=viewer.maya_main_window())
    _dialog.show()
    return _dialog
