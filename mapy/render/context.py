from dataclasses import dataclass

from mapy.common import ScreenSize
from mapy.geo_util import Box, Transformer
from mapy.render.renderer import RenderBackend


@dataclass
class RenderContext:
    render_backend: RenderBackend
    transformer: Transformer
    bbox: Box
    screen_size: ScreenSize
