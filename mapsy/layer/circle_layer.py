from dataclasses import dataclass

from shapely import (
    MultiPoint,
    Point,
)

from mapsy.color import Color, Colors
from mapsy.render.context import RenderContext


@dataclass
class CircleItem:
    geometry: Point | MultiPoint
    color: Color = Colors.BLACK
    radius: float = 1
    line_color: Color = Colors.BLACK
    line_width: float = 0


class CircleLayer:
    def __init__(self, items: list[CircleItem]) -> None:
        self.items = items

    def render(self, context: RenderContext) -> None:
        for item in self.items:
            geometry = context.transformer.transform_to_image_crs(item.geometry)
            if isinstance(geometry, MultiPoint):
                for point in geometry.geoms:
                    context.render_backend.draw_point(
                        point=point,
                        radius=item.radius,
                        color=item.color,
                        outline_color=item.line_color,
                        outline_width=item.line_width,
                    )
            else:
                context.render_backend.draw_point(
                    point=geometry,
                    radius=item.radius,
                    color=item.color,
                    outline_color=item.line_color,
                    outline_width=item.line_width,
                )
