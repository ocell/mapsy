from dataclasses import dataclass
from affine import Affine
from shapely import MultiPoint, Point, affinity

from mapsy.color import Color
from mapsy.common import FontSlant, FontWeight, TextAnchor
from mapsy.icon.icon import Icon
from mapsy.layer.layer import Layer
from mapsy.common import IconAlign


from mapsy.render.context import RenderContext


@dataclass
class SymbolItem:
    geometry: Point | MultiPoint
    icon: Icon | None = None
    icon_offset: tuple[float, float] = (0, 0)
    icon_size: float = 1
    text: str | None = None
    text_offset: tuple[float, float] = (0, 0)
    text_font: str = "arial"
    text_size: float = 12
    text_color: Color | None = Color(0, 0, 0)
    text_slant: FontSlant | None = None
    text_weight: FontWeight | None = None
    text_anchor: TextAnchor | None = None
    text_outline_width: float | None = None
    text_outline_color: Color | None = None


class SymbolLayer(Layer):
    items: list[SymbolItem]

    def __init__(self, symbols: list[SymbolItem]) -> None:
        self.items = symbols
        super().__init__()

    @staticmethod
    def _icon_to_raw_offset(icon: Icon) -> tuple[float, float]:
        match icon.alignment:
            case IconAlign.TOP_LEFT:
                return 0, 0
            case IconAlign.TOP_CENTER:
                return -icon.size[0] / 2, 0
            case IconAlign.TOP_RIGHT:
                return -icon.size[0], 0
            case IconAlign.CENTER_LEFT:
                return 0, -icon.size[1] / 2
            case IconAlign.CENTER:
                return -icon.size[0] / 2, -icon.size[1] / 2
            case IconAlign.CENTER_RIGHT:
                return -icon.size[0], -icon.size[1] / 2
            case IconAlign.BOTTOM_LEFT:
                return 0, -icon.size[1]
            case IconAlign.BOTTOM_CENTER:
                return -icon.size[0] / 2, -icon.size[1]
            case IconAlign.BOTTOM_RIGHT:
                return -icon.size[0], -icon.size[1]
            case _:
                return 0, 0

    @staticmethod
    def _icon_to_offset(icon: Icon, icon_size: float) -> tuple[float, float]:
        x, y = SymbolLayer._icon_to_raw_offset(
            icon,
        )
        return x * icon_size, y * icon_size

    def render(self, context: RenderContext) -> None:

        def render_point(point: Point, symbol_item: SymbolItem) -> None:
            if symbol_item.icon:
                alignment_offset = self._icon_to_offset(
                    symbol_item.icon, symbol_item.icon_size
                )
                offset = (
                    symbol_item.icon_offset[0] + alignment_offset[0],
                    symbol_item.icon_offset[1] + alignment_offset[1],
                )

                context.render_backend.draw_image(
                    image=symbol_item.icon.data,
                    affine=self.affine_for_point_and_offset(
                        point,
                        offset,
                        scale=symbol_item.icon_size,
                    ),
                )
            if symbol_item.text:
                context.render_backend.draw_text(
                    text=symbol_item.text,
                    point=(
                        affinity.translate(
                            point,
                            xoff=symbol_item.text_offset[0],
                            yoff=symbol_item.text_offset[1],
                        )
                        if symbol_item.text_offset
                        else point
                    ),
                    color=symbol_item.text_color,
                    font=symbol_item.text_font,
                    font_size=symbol_item.text_size,
                    font_slant=symbol_item.text_slant,
                    font_weight=symbol_item.text_weight,
                    outline_color=symbol_item.text_outline_color,
                    outline_width=symbol_item.text_outline_width,
                    anchor=symbol_item.text_anchor,
                )

        for item in self.items:
            geometry = context.transformer.transform_to_image_crs(item.geometry)

            if isinstance(geometry, MultiPoint):
                for point in geometry.geoms:
                    render_point(point, item)
            else:
                render_point(geometry, item)

    def affine_for_point_and_offset(
        self,
        point: Point,
        offset: tuple[float, float],
        scale: float = 1,
    ) -> Affine:
        x, y = point.coords.xy[0][0] + offset[0], point.coords.xy[1][0] + offset[1]
        if 1000 > x > 0 and 1000 > y > 0:
            print(f"point {x}, {y} offset {offset} scale {scale}")

        return Affine(scale, 0, x, 0, scale, y)
