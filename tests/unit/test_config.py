import tempfile
import unittest
from pathlib import Path

from router_os.config import ConfigLoadError, load_config

VALID = """
router:
  hostname: test-router
  router_id: 10.0.0.1
nls:
  enabled: true
interfaces:
  - name: eth0
    role: lan
"""


class ConfigTests(unittest.TestCase):
    def test_valid_configuration_loads(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "router.yaml"
            path.write_text(VALID, encoding="utf-8")
            config = load_config(path)
        self.assertEqual(config.router.router_id, "10.0.0.1")
        self.assertTrue(config.nls.enabled)
        self.assertEqual(config.interfaces[0].name, "eth0")

    def test_invalid_router_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "router.yaml"
            path.write_text(VALID.replace("10.0.0.1", "invalid"), encoding="utf-8")
            with self.assertRaises(ConfigLoadError):
                load_config(path)


if __name__ == "__main__":
    unittest.main()
