import importlib.util
from pathlib import Path


ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def test_supported_versions_are_current():
    assert installer.SUPPORTED_MAYA_MIN == 2022
    assert installer.SUPPORTED_MAX_MIN == 2024


def test_detection_shape():
    result = installer.detect_hosts()
    assert set(result) == {"maya", "3dsmax"}
    assert all(isinstance(version, int) for versions in result.values() for version in versions)
