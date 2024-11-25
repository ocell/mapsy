from mapsy.color import Color
from mapsy.layer.layer import Layer
from mapsy.render.context import RenderContext


class BackgroundLayer(Layer):
    def __init__(self, color: Color) -> None:
        self.color = color
        super().__init__()

    def render(self, context: RenderContext) -> None:
        context.render_backend.draw_rectangle(self.color, 0, 0, *context.screen_size)
