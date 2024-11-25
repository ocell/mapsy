import math
from typing import Protocol
from mapsy.common import ScreenSize
from mapsy.geo_util import Transformer
from mapsy.render.cairo_backend import CairoBackend
from mapsy.layer.layer import Layer


from mapsy.layer.raster_layer import Box
from mapsy.render.context import RenderContext
from mapsy.render.renderer import Surface


class RenderMode(Protocol):
    bbox: Box
    screen_size: ScreenSize


class FixedBBox(RenderMode):
    """Use this class to render a map with a specific bounding box and pixel count.

    The aspect ratio of the render depends on the aspect ratio of the bounding box.
    For this reason, the pixel count is used to calculate the x and y sizes of the
    render. screen_size is calculated based on the pixel count and the aspect
    ratio of the bounding box. bbox is the bounding box that will be rendered.
    """

    def __init__(self, bbox: Box, pixel_count: int) -> None:
        self.bbox = bbox
        self.pixel_count = pixel_count
        xy_bbox = bbox.to_xy()
        ratio = xy_bbox.aspect_ratio

        y_size = math.sqrt(pixel_count / ratio)
        x_size = y_size * ratio

        self.screen_size = ScreenSize(round(x_size), round(y_size))


class FixedScreenSize(RenderMode):
    """Use this class to render a map with a specific screen size and area of interest.

    The aspect ratio of the render depends on the aspect ratio of the screen size.
    For this reason, the bounding box is calculated based on the area of interest and
    the screen size. The area of interest is guaranteed to be fully visible in the
    render. Padding is added to the bounding box to match the aspect ratio of the screen
    size.
    """

    def __init__(self, area_of_interest: Box, size: ScreenSize) -> None:
        self.screen_size = size

        self.bbox = (
            area_of_interest.to_xy()
            .with_new_aspect_ratio_as_padding(size.aspect_ratio)
            .to_lng_lat()
        )


class Map:
    def __init__(self) -> None:
        self.layers: list[Layer] = []

    def add_layer(self, layer: str) -> None:
        self.layers.append(layer)

    def render(self, render_mode: RenderMode) -> Surface:
        bbox = render_mode.bbox
        screen_size = render_mode.screen_size
        render_backend = CairoBackend(screen_size)
        transformer = Transformer(bbox, screen_size)

        context = RenderContext(
            bbox=bbox,
            transformer=transformer,
            render_backend=render_backend,
            screen_size=screen_size,
        )

        for layer in self.layers:
            layer.render(context)

        return render_backend.surface
