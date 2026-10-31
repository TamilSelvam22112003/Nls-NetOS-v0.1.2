"""Network inventory change detector."""
class ChangeDetector:
    def diff(self, old, new):
        old, new = dict(old), dict(new)
        return {"added": new.keys() - old.keys(), "removed": old.keys() - new.keys()}
