import tempfile
import unittest
from pathlib import Path

from router_os.application import BootPhase, RouterApplication

CONFIG = """
router:
  hostname: integration-router
  router_id: 10.0.0.2
nls:
  enabled: true
interfaces: []
"""


class BootTests(unittest.TestCase):
    def test_boot_reaches_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "router.yaml"
            path.write_text(CONFIG, encoding="utf-8")
            app = RouterApplication(path)
            app.boot()
            try:
                self.assertEqual(app.phase, BootPhase.READY)
            finally:
                app.stop()


if __name__ == "__main__":
    unittest.main()
