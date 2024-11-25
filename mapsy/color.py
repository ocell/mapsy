import colorsys
from dataclasses import dataclass


@dataclass
class Color:
    r: float
    g: float
    b: float
    a: float = 1.0

    @property
    def h(self) -> float:
        self._ensure_hsv_exists()
        return self.hsv[0]

    @property
    def s(self) -> float:
        self._ensure_hsv_exists()
        return self.hsv[2]

    @property
    def v(self) -> float:
        self._ensure_hsv_exists()
        return self.hsv[3]

    @property
    def hsv(self) -> tuple[float, float, float]:
        self._ensure_hsv_exists()
        return self.hsv

    def _ensure_hsv_exists(self):
        if self._hsv is None:
            self._hsv = colorsys.rgb_to_hsv(self.r, self.g, self.b)

    def float_rgb(self) -> tuple[float, float, float]:
        return self.r, self.g, self.b

    def float_rgba(self) -> tuple[float, float, float, float]:
        return self.r, self.g, self.b, self.a

    @staticmethod
    def from_hsv(h: float, s: float, v: float, a: float = 1.0):
        return Color(*colorsys.hsv_to_rgb(h, s, v), a)

    def darken(self, amount: float) -> "Color":
        factor = 1 - amount
        return Color(
            self.r * factor,
            self.g * factor,
            self.b * factor,
            self.a,
        )

    def with_alpha(self, alpha: float) -> "Color":
        return Color(self.r, self.g, self.b, alpha)

    def lighten(self, factor: float) -> "Color":
        return Color(
            self.r + (1 - self.r) * factor,
            self.g + (1 - self.g) * factor,
            self.b + (1 - self.b) * factor,
            self.a,
        )


class Colors:
    BLACK = Color(0, 0, 0)
    TRANSPARENT = Color(0, 0, 0, 0)
    WHITE = Color(1, 1, 1)
    BLUE = Color(0, 0, 1)
    RED = Color(1, 0, 0)
    GREEN = Color(0, 1, 0)
    YELLOW = Color(1, 1, 0)
    CYAN = Color(0, 1, 1)
    MAGENTA = Color(1, 0, 1)
    ORANGE = Color(1, 0.5, 0)
    PURPLE = Color(0.5, 0, 1)
    TEAL = Color(0, 0.5, 1)
    LIME = Color(0.5, 1, 0)
    PINK = Color(1, 0.5, 1)
    BROWN = Color(0.5, 0.25, 0)
    GRAY = Color(0.5, 0.5, 0.5)
    LIGHT_GRAY = Color(0.75, 0.75, 0.75)
    DARK_GRAY = Color(0.25, 0.25, 0.25)
    OLIVE = Color(0.5, 0.5, 0)
    MAROON = Color(0.5, 0, 0)
    NAVY = Color(0, 0, 0.5)
    SILVER = Color(0.75, 0.75, 0.75)
    GOLD = Color(1, 0.843, 0)
    SKY_BLUE = Color(0.529, 0.808, 0.922)
