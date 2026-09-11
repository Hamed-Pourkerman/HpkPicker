"""Autodesk Maya adapter (Maya 2022+ / Python 3 / PySide2)."""

from .base import NullHost


class MayaHost(NullHost):
    name = "maya"

    def __init__(self):
        from maya import cmds, OpenMayaUI
        import shiboken2
        from PySide2 import QtWidgets
        self.cmds = cmds
        self._ui = OpenMayaUI
        self._shiboken = shiboken2
        self._widgets = QtWidgets

    def main_window(self):
        ptr = self._ui.MQtUtil.mainWindow()
        return self._shiboken.wrapInstance(int(ptr), self._widgets.QWidget) if ptr else None

    def select_items(self, items, prefix=""):
        self.cmds.select(clear=True)
        for item in items:
            for object_name in item.itemDict.get("object_list", []):
                nodes = self.cmds.ls("*:" + object_name) or self.cmds.ls("*" + object_name)
                for node in nodes:
                    if not prefix or prefix in node:
                        self.cmds.select(node, add=True)

    def capture_selection(self):
        return [name.rsplit(":", 1)[-1] for name in self.cmds.ls(selection=True) or []]

    def run_script(self, script):
        for command in (script or "").splitlines():
            if command.strip():
                self.cmds.evalDeferred(command)
