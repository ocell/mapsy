from dataclasses import dataclass

from shapely import MultiPolygon, Polygon

from mapsy.color import Color
from mapsy.render.context import RenderContext


@dataclass
class FillItem:
    geometry: Polygon | MultiPolygon
    color: Color
    line_color: Color
    line_width: int = 0


class FillLayer:
    def __init__(self, items: list[FillItem]) -> None:
        self.items = items

    def render(self, context: RenderContext) -> None:
        for item in self.items:
            polygon_in_img_crs = context.transformer.transform_to_image_crs(
                item.geometry
            )
            if isinstance(polygon_in_img_crs, MultiPolygon):
                for poly in polygon_in_img_crs.geoms:
                    context.render_backend.draw_polygon(
                        polygon=poly,
                        line_color=item.line_color,
                        fill_color=item.color,
                        line_width=item.line_width,
                    )
            else:
                context.render_backend.draw_polygon(
                    polygon=polygon_in_img_crs,
                    line_color=item.line_color,
                    fill_color=item.color,
                    line_width=item.line_width,
                )
