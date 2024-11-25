from dataclasses import dataclass

from shapely import LineString, MultiLineString
from mapy.common import LineCap, LineJoin
from mapy.layer.layer import Layer
from mapy.render.context import RenderContext


@dataclass
class LineItem:
    """Dataclass representing a line item

    Limitations:
    If a outline_color/width is set, setting a color with an alpha value lead to
    unexpected results.
    """

    geometry: LineString | MultiLineString
    color: str | None = None
    width: float | None = 1
    cap: LineCap | None = LineCap.BUTT
    join: LineJoin | None = LineJoin.MITER
    outline_color: str | None = None
    outline_width: float | None = None


class LineLayer(Layer):
    def __init__(self, lines: list[LineItem]) -> None:
        self.items = lines

    def render(self, context: RenderContext) -> None:
        def render_line(geom: LineString, item: LineItem) -> None:
            context.render_backend.draw_line(
                geom,
                color=item.color,
                width=item.width,
                cap=item.cap,
                join=item.join,
                outline_color=item.outline_color,
                outline_width=item.outline_width,
            )

        for line_item in self.items:
            geometry = context.transformer.transform_to_image_crs(line_item.geometry)

            if isinstance(geometry, MultiLineString):
                for geom in geometry.geoms:
                    render_line(geom, line_item)
            else:
                render_line(geometry, line_item)
