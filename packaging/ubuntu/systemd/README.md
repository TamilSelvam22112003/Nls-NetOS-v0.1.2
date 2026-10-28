# systemd service design

Future services should run with least privilege, use restrictive filesystem/capability settings, protect credentials, and stop safely. A unit must not be enabled by default before protocol and operational behavior are reviewed.
