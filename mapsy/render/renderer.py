from typing import Protocol, Tuple
from affine import Affine
from cairo import FontWeight
from shapely import LineString, Point, Polygon

from mapsy.color import Color
from mapsy.common import FontSlant, ImageFilter, LineCap, LineJoin, TextAnchor


class Surface(Protocol):
    def write_to_png(self, path: str) -> None: ...


class RenderBackend(Protocol):
    @property
    def surface(self) -> Surface: ...

    def combine_images(
        self,
        images: list[bytes],
        origins: list[tuple[int, int]],
        output_shape: tuple[int, int],
    ) -> Surface: ...

    def draw_image(
        self,
        image: bytes | Surface,
        affine: Affine,
        image_filter: ImageFilter = ImageFilter.BEST,
    ) -> None: ...

    def draw_rectangle(
        self, color: Color, x: float, y: float, width: float, height: float
    ) -> None: ...

    def draw_polygon(
        self,
        polygon: Polygon,
        line_color: Color = None,
        line_width: float = 0,
        fill_color: Color = None,
    ) -> None: ...

    def draw_line(
        self,
        line: LineString,
        color: Color,
        width: float,
        cap: LineCap = LineCap.BUTT,
        join: LineJoin = LineJoin.MITER,
        outline_color: Color = None,
        outline_width: float = 0,
    ) -> None: ...

    def draw_text(
        self,
        text: str,
        point: Point,
        color: Color,
        font: str,
        anchor: TextAnchor = TextAnchor.LEFT,
        font_size: float = 12,
        font_weight: FontWeight = FontWeight.NORMAL,
        font_slant: FontSlant = FontSlant.NORMAL,
        outline_width: float = 0,
        outline_color: Color = None,
        background_color: Color = None,
        background_padding: float = 0,
    ) -> None: ...

    def draw_point(
        self,
        point: Point,
        radius: float,
        color: Color | None,
        outline_color: Color | None = None,
        outline_width: float = 0,
    ) -> None: ...

    def point_to_xy(self, point: Point) -> Tuple[float, float]: ...
