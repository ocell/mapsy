from enum import Enum
from typing import NamedTuple


class MapsyInfo:
    AGENT_NAME = "mapsy"
    VERSION = "0.1.0"


class LineCap(Enum):
    BUTT = "butt"
    ROUND = "round"
    SQUARE = "square"


class LineJoin(Enum):
    BEVEL = "bevel"
    ROUND = "round"
    MITER = "miter"


class FontWeight(Enum):
    BOLD = "bold"
    NORMAL = "normal"


class IconAlign(Enum):
    TOP_LEFT = "top-left"
    TOP_CENTER = "top-center"
    TOP_RIGHT = "top-right"
    CENTER_LEFT = "center-left"
    CENTER = "center"
    CENTER_RIGHT = "center-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_CENTER = "bottom-center"
    BOTTOM_RIGHT = "bottom-right"


class TextAnchor(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"


class FontSlant(Enum):
    NORMAL = "normal"
    ITALIC = "italic"
    OBLIQUE = "oblique"


class SymbolAlgin(Enum):
    top_left = "top_left"
    top_center = "top_center"
    top_right = "top_right"
    center_left = "center_left"
    center = "center"
    center_right = "center_right"
    bottom_left = "bottom_left"
    bottom_center = "bottom_center"
    bottom_right = "bottom_right"


class ImageFilter(Enum):
    BEST = "best"
    BILINEAR = "bilinear"
    FAST = "fast"
    GAUSSIAN = "gaussian"
    GOOD = "good"
    NEAREST = "nearest"


class ScreenSize(NamedTuple):
    width: int
    height: int

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height
