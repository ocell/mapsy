from cairo import FontSlant
from shapely import Point
from mapsy.color import Color, Colors
from mapsy.common import FontWeight, TextAnchor
from mapsy.layer.layer import Layer
from mapsy.render.context import RenderContext


class Attribution(Layer):
    def __init__(
        self,
        attribution: list[str] | str,
        font: str = "arial",
        size: float = 14,
        color: Color = Colors.BLACK,
        slant: FontSlant | None = None,
        weight: FontWeight | None = None,
        outline_width: float = 1,
        padding: float = 2,
        text_outline_color: Color | None = None,
        background_color: Color | None = Color(1, 1, 1, 0.6),
        background_padding: float = 2,
    ) -> None:
        self.attributions = (
            attribution if isinstance(attribution, list) else [attribution]
        )
        self.font = font
        self.size = size
        self.color = color
        self.slant = slant
        self.weight = weight
        self.padding = padding
        self.outline_width = outline_width
        self.outline_color = text_outline_color
        self.background_color = background_color
        self.background_padding = background_padding

    def render(self, context: RenderContext) -> None:

        text = " ".join(self.attributions)
        x, y = context.screen_size
        context.render_backend.draw_text(
            text=text,
            point=Point(x - self.padding, y - self.padding),
            color=self.color,
            font=self.font,
            font_size=self.size,
            font_slant=self.slant,
            font_weight=self.weight,
            outline_width=self.outline_width,
            outline_color=self.outline_color,
            anchor=TextAnchor.BOTTOM_RIGHT,
            background_color=self.background_color,
            background_padding=self.background_padding,
        )
