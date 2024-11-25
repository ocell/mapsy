from mapy.color import Color
from mapy.layer.layer import Layer
from mapy.render.context import RenderContext


class BackgroundLayer(Layer):
    def __init__(self, color: Color) -> None:
        self.color = color
        super().__init__()

    def render(self, context: RenderContext) -> None:
        context.render_backend.draw_rectangle(self.color, 0, 0, *context.screen_size)
