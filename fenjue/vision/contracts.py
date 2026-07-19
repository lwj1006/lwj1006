from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class ComposerLayout(str, Enum):
    MISSING = "missing"
    NEW_CHAT_CENTERED = "new_chat_centered"
    ACTIVE_CHAT_BOTTOM = "active_chat_bottom"
    IMAGE_VIEWER = "image_viewer"


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def center(self) -> tuple[int, int]:
        return self.x + self.width // 2, self.y + self.height // 2

    def clipped(self, screen_width: int, screen_height: int) -> "Rect":
        left = max(0, min(screen_width - 1, self.x))
        top = max(0, min(screen_height - 1, self.y))
        right = max(left + 1, min(screen_width, self.right))
        bottom = max(top + 1, min(screen_height, self.bottom))
        return Rect(left, top, right - left, bottom - top)


@dataclass(frozen=True)
class ScreenState:
    screen_width: int
    screen_height: int
    layout: ComposerLayout = ComposerLayout.MISSING
    composer: Rect | None = None
    plus_button: Rect | None = None
    input_box: Rect | None = None
    action_button: Rect | None = None
    attachment_menu: Rect | None = None
    add_file_row: Rect | None = None
    create_image_row: Rect | None = None
    model_selector: Rect | None = None
    model_menu: Rect | None = None
    model_high_row: Rect | None = None
    file_name_input: Rect | None = None
    viewer_close_button: Rect | None = None
    attachment_boxes: tuple[Rect, ...] = field(default_factory=tuple)
    attachment_count: int = 0
    action_kind: str = "missing"
    input_ink_ratio: float = 0.0
    confidence: float = 0.0
    diagnostics: tuple[str, ...] = field(default_factory=tuple)

    @property
    def page_ready(self) -> bool:
        return self.composer is not None and self.input_box is not None


class ScreenVision(Protocol):
    def inspect(self) -> ScreenState:
        ...

    def save_diagnostic(self, label: str) -> str:
        ...
