import io
import math

import cairo
from affine import Affine

from cairo import Context, ImageSurface
from PIL import Image
from shapely import LineString, Point, Polygon

from mapsy.color import Color
from mapsy.common import (
    FontSlant,
    FontWeight,
    ImageFilter,
    LineCap,
    LineJoin,
    TextAnchor,
)
from cairo import FontSlant as FontSlantCairo
from cairo import FontWeight as FontWeightCairo

from mapsy.render.renderer import RenderBackend, Surface

_font_weight_to_cairo = {
    FontWeight.NORMAL: cairo.FONT_WEIGHT_NORMAL,
    FontWeight.BOLD: cairo.FONT_WEIGHT_BOLD,
}

_font_slant_to_cairo = {
    FontSlant.NORMAL: cairo.FONT_SLANT_NORMAL,
    FontSlant.ITALIC: cairo.FONT_SLANT_ITALIC,
    FontSlant.OBLIQUE: cairo.FONT_SLANT_OBLIQUE,
}

_line_cap_to_cairo = {
    LineCap.BUTT: cairo.LINE_CAP_BUTT,
    LineCap.ROUND: cairo.LINE_CAP_ROUND,
    LineCap.SQUARE: cairo.LINE_CAP_SQUARE,
}

_line_join_to_cairo = {
    LineJoin.BEVEL: cairo.LINE_JOIN_BEVEL,
    LineJoin.ROUND: cairo.LINE_JOIN_ROUND,
    LineJoin.MITER: cairo.LINE_JOIN_MITER,
}


class CairoBackend(RenderBackend):
    def __init__(self, shape: tuple[int, int]) -> None:
        self.shape = shape
        self._reset(shape)

    def _reset(self, shape: tuple[int, int]) -> None:
        self._surface = ImageSurface(cairo.FORMAT_ARGB32, *shape)
        self.context = Context(self.surface)
        self.context.set_antialias(cairo.ANTIALIAS_BEST)

    def transformer(self, affine: Affine) -> cairo.Matrix:
        return cairo.Matrix(
            xx=affine.a, xy=affine.b, x0=affine.c, yy=affine.e, yx=affine.d, y0=affine.f
        )

    @property
    def surface(self) -> Surface:
        return self._surface

    def combine_images(
        self,
        images: list[bytes],
        origins: list[tuple[int, int]],
        output_shape: tuple[int, int],
    ) -> Surface:
        assert len(images) == len(
            origins
        ), "Images and origins must have the same length"

        surface = ImageSurface(cairo.FORMAT_ARGB32, *output_shape)
        context = Context(surface)
        for image, offset in zip(images, origins):
            context.save()
            image_surface = self._to_image_surface(image)
            context.translate(*offset)
            context.set_source_surface(image_surface)
            context.paint()
            context.restore()
        return surface

    def draw_image(
        self,
        image: bytes | Surface,
        affine: Affine,
        image_filter: ImageFilter = ImageFilter.BEST,
    ) -> None:
        surface = self._to_image_surface(image) if isinstance(image, bytes) else image
        matrix = cairo.Matrix(
            xx=affine.a,
            xy=affine.b,
            x0=affine.c,
            yy=affine.e,
            yx=affine.d,
            y0=affine.f,
        )
        self.context.save()
        self.context.transform(matrix)
        self.context.set_source_surface(surface)
        source = self.context.get_source()
        filter = getattr(cairo, f"FILTER_{image_filter.value.upper()}")
        source.set_filter(filter)

        self.context.paint()
        self.context.restore()

    def draw_polygon(
        self,
        polygon: Polygon,
        line_color: Color = None,
        line_width: float = 0,
        fill_color: Color = None,
    ) -> None:
        context = self.context
        outlines_xys = polygon.exterior.coords
        holes_xys = [hole.coords for hole in polygon.interiors]

        def draw_paths(color: Color):
            context.set_source_rgba(*color.float_rgba())
            for x, y in outlines_xys:
                context.line_to(x, y)

            for hole_xys in holes_xys:
                context.new_sub_path()
                for x, y in hole_xys:
                    context.line_to(x, y)

        context.new_path()
        if fill_color:
            draw_paths(fill_color)
            context.fill()

        if line_width > 0:
            context.set_line_width(line_width)
            context.set_line_join(cairo.LINE_JOIN_ROUND)

            draw_paths(line_color)
            context.stroke()

    def draw_line(
        self,
        line: LineString,
        color: Color,
        width: float,
        cap: LineCap = LineCap.BUTT,
        join: LineJoin = LineJoin.ROUND,
        outline_color: Color = None,
        outline_width: float = 0,
    ) -> None:
        context = self.context
        context.new_path()
        for x, y in line.coords:
            context.line_to(x, y)

        context.set_line_cap(_line_cap_to_cairo[cap])
        context.set_line_join(_line_join_to_cairo[join])
        if outline_width and outline_color:
            context.set_line_width(width + outline_width * 2)
            context.set_source_rgba(*outline_color.float_rgba())
            context.stroke_preserve()
        context.set_source_rgba(*color.float_rgba())
        context.set_line_width(width)
        context.stroke()

    def draw_rectangle(
        self, color: Color, x: float, y: float, width: float, height: float
    ) -> None:
        context = self.context
        context.set_source_rgba(*color.float_rgba())
        context.rectangle(x, y, width, height)
        context.fill()

    def draw_text(
        self,
        text: str,
        point: Point,
        color: Color,
        font: str,
        font_size: float = 12,
        font_weight: FontWeight = FontWeight.NORMAL,
        font_slant: FontSlant = FontSlant.NORMAL,
        outline_width: float = 0,
        outline_color: Color = None,
        anchor: TextAnchor = TextAnchor.BOTTOM_LEFT,
        background_color: Color = None,
        background_padding: float = 0,
    ) -> None:
        context = self.context
        context.set_source_rgba(*color.float_rgba())
        context.move_to(*self.point_to_xy(point))
        anchor = anchor or TextAnchor.BOTTOM_LEFT

        cairo_weight = (
            _font_weight_to_cairo[font_weight]
            if font_weight
            else FontWeightCairo.NORMAL
        )
        cairo_slant = (
            _font_slant_to_cairo[font_slant] if font_slant else FontSlantCairo.NORMAL
        )
        context.select_font_face(font, cairo_slant, cairo_weight)
        context.set_font_size(font_size)

        extends = context.text_extents(text)
        current_x, current_y = context.get_current_point()

        match anchor:
            case TextAnchor.BOTTOM_LEFT:
                pass  # already set as the default
            case TextAnchor.BOTTOM:
                context.move_to(current_x - extends.width / 2, current_y)
            case TextAnchor.BOTTOM_RIGHT:
                context.move_to(current_x - extends.width, current_y)

            case TextAnchor.LEFT:
                context.move_to(current_x, current_y + extends.height / 2)
            case TextAnchor.CENTER:
                context.move_to(
                    current_x - extends.width / 2,
                    current_y + extends.height / 2,
                )
            case TextAnchor.RIGHT:
                context.move_to(
                    current_x - extends.width,
                    current_y + extends.height / 2,
                )

            case TextAnchor.TOP_LEFT:
                context.move_to(current_x, current_y + extends.height)
            case TextAnchor.TOP:
                context.move_to(
                    current_x - extends.width / 2, current_y + extends.height
                )
            case TextAnchor.TOP_RIGHT:
                context.move_to(current_x - extends.width, current_y + extends.height)

            case _:
                pass

        if background_color:
            current_x, current_y = context.get_current_point()
            context.rectangle(
                current_x - background_padding,
                current_y - extends.height * 0.8 - background_padding,
                extends.width + background_padding * 2,
                extends.height + background_padding * 2,
            )
            context.set_source_rgba(*background_color.float_rgba())
            context.fill()
            context.move_to(current_x, current_y)
        context.text_path(text)
        if outline_width and outline_color:
            context.set_line_width(outline_width * 2)
            context.set_source_rgba(*outline_color.float_rgba())
            context.set_line_join(cairo.LINE_JOIN_ROUND)
            context.stroke_preserve()

        context.set_source_rgba(*color.float_rgba())
        context.fill()

    def draw_point(
        self,
        point: Point,
        radius: float,
        color: Color | None,
        outline_color: Color | None = None,
        outline_width: float = 0,
    ) -> None:
        context = self.context
        context.new_path()

        context.set_source_rgba(*color.float_rgba())
        context.arc(*self.point_to_xy(point), radius, 0, 2 * math.pi)
        context.fill_preserve()
        if outline_width and outline_color:
            context.set_line_width(outline_width)
            context.set_source_rgba(*outline_color.float_rgba())
            context.stroke()

    def point_to_xy(self, point: Point) -> tuple[float, float]:
        return point.coords.xy[0][0], point.coords.xy[1][0]

    def _to_image_surface(self, image_data: bytes) -> ImageSurface:
        image = Image.open(io.BytesIO(image_data))
        if image.format == "PNG":
            return cairo.ImageSurface.create_from_png(io.BytesIO(image_data))
        png_bytes = io.BytesIO()
        image.save(png_bytes, format="PNG")
        png_bytes.flush()
        png_bytes.seek(0)
        return cairo.ImageSurface.create_from_png(png_bytes)
