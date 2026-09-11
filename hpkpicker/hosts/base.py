"""Host-independent adapter contract and offline fallback."""


class NullHost:
    name = "standalone"

    def main_window(self):
        return None

    def select_items(self, _items, _prefix=""):
        return []

    def capture_selection(self):
        return []

    def run_script(self, _script):
        return None
