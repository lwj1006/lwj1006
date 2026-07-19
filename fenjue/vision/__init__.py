"""Optional screen-vision automation for the Fenjue runtime.

The legacy coordinate workflow remains the default.  Importing this package has
no side effects; callers must explicitly activate it with ``--vision``.
"""

from .contracts import ComposerLayout, Rect, ScreenState, ScreenVision

__all__ = ["ComposerLayout", "Rect", "ScreenState", "ScreenVision"]
