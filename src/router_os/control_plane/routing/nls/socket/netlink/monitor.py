"""Netlink event monitoring boundary."""
class NetlinkMonitor:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
