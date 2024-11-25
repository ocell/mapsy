import mapsy
from shapely import Point

from test.util import assert_render_equality


def test_symbol_layer(tmp_path):
    items = [
        mapsy.SymbolItem(
            geometry=Point(0.5, 0.5),
            icon=mapsy.Icons.PIN_24,
            icon_size=1,
            text="Hello",
            text_size=20,
            text_color=mapsy.Color(0, 0, 0),
            text_outline_width=1,
            text_outline_color=mapsy.Color(1, 1, 1),
        ),
        mapsy.SymbolItem(
            geometry=Point(0.8, 0.8),
            icon=mapsy.Icons.PIN_48,
            icon_size=0.5,
        ),
    ]
    layer = mapsy.SymbolLayer(items)
    assert layer.items == items

    with assert_render_equality(tmp_path, "test_symbol_layer.png") as map:
        map.add_layer(layer)


def test_text_alignment(tmp_path):
    bg = mapsy.BackgroundLayer(color=mapsy.Colors.WHITE)
    point = mapsy.CircleLayer(
        [
            mapsy.CircleItem(
                geometry=Point(0.5, 0.5),
                color=mapsy.Colors.RED,
                radius=4,
                line_color=mapsy.Colors.BLACK,
                line_width=2,
            )
        ]
    )
    for anchor in mapsy.TextAnchor:
        anchor_str = str(anchor.value)
        items = [
            mapsy.SymbolItem(
                geometry=Point(0.5, 0.5),
                text=anchor_str.upper(),
                text_size=11,
                text_color=mapsy.Colors.WHITE,
                text_outline_width=1,
                text_outline_color=mapsy.Colors.BLACK,
                text_anchor=anchor,
            )
        ]
        layer = mapsy.SymbolLayer(items)
        with assert_render_equality(
            tmp_path, f"test_text_anchor_{anchor_str}.png", size=(180, 40)
        ) as map:
            map.add_layer(bg)
            map.add_layer(point)
            map.add_layer(layer)
