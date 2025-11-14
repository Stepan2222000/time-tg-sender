"""
Debug module stub for TLAPI
Minimal implementation to satisfy imports
"""

# Disable debug mode by default
IS_DEBUG_MODE = False


class DebugMethod:
    """Stub for debug method wrapper"""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
