import mapy
from shapely import Point

from test.util import assert_render_equality


def test_symbol_layer(tmp_path):
    items = [
        mapy.SymbolItem(
            geometry=Point(0.5, 0.5),
            icon=mapy.Icons.PIN_24,
            icon_size=1,
            text="Hello",
            text_size=20,
            text_color=mapy.Color(0, 0, 0),
            text_outline_width=1,
            text_outline_color=mapy.Color(1, 1, 1),
        ),
        mapy.SymbolItem(
            geometry=Point(0.8, 0.8),
            icon=mapy.Icons.PIN_48,
            icon_size=0.5,
        ),
    ]
    layer = mapy.SymbolLayer(items)
    assert layer.items == items

    with assert_render_equality(tmp_path, "test_symbol_layer.png") as map:
        map.add_layer(layer)


def test_text_alignment(tmp_path):
    bg = mapy.BackgroundLayer(color=mapy.Colors.WHITE)
    point = mapy.CircleLayer(
        [
            mapy.CircleItem(
                geometry=Point(0.5, 0.5),
                color=mapy.Colors.RED,
                radius=4,
                line_color=mapy.Colors.BLACK,
                line_width=2,
            )
        ]
    )
    for anchor in mapy.TextAnchor:
        anchor_str = str(anchor.value)
        items = [
            mapy.SymbolItem(
                geometry=Point(0.5, 0.5),
                text=anchor_str.upper(),
                text_size=11,
                text_color=mapy.Colors.WHITE,
                text_outline_width=1,
                text_outline_color=mapy.Colors.BLACK,
                text_anchor=anchor,
            )
        ]
        layer = mapy.SymbolLayer(items)
        with assert_render_equality(
            tmp_path, f"test_text_anchor_{anchor_str}.png", size=(180, 40)
        ) as map:
            map.add_layer(bg)
            map.add_layer(point)
            map.add_layer(layer)
