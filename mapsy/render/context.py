from dataclasses import dataclass

from mapsy.common import ScreenSize
from mapsy.geo_util import Box, Transformer
from mapsy.render.renderer import RenderBackend


@dataclass
class RenderContext:
    render_backend: RenderBackend
    transformer: Transformer
    bbox: Box
    screen_size: ScreenSize
