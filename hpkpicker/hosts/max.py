"""Autodesk 3ds Max adapter (2024+ / Python 3 / PySide2)."""

from .base import NullHost


class MaxHost(NullHost):
    name = "3dsmax"

    def __init__(self):
        from pymxs import runtime as rt
        from qtmax import GetQMaxMainWindow
        self.rt = rt
        self._main_window = GetQMaxMainWindow()

    def main_window(self):
        return self._main_window

    def select_items(self, items, _prefix=""):
        nodes = []
        for item in items:
            nodes.extend(item.itemDict.get("object_list", []))
        resolved = [self.rt.getNodeByName(name) for name in nodes]
        self.rt.select([node for node in resolved if node])
        return resolved

    def capture_selection(self):
        return [str(node.name) for node in self.rt.selection]

    def run_script(self, script):
        if script and script.strip():
            self.rt.execute(script)
