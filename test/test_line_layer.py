import mapsy
from shapely import LineString, transform

from test.util import assert_render_equality


def test_line_layer(tmp_path):
    items = [
        mapsy.LineItem(
            geometry=LineString([(0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)]),
            color=mapsy.Color(1, 0, 0),
            width=1,
        ),
        mapsy.LineItem(
            geometry=LineString([(0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)]),
            color=mapsy.Color(0, 1, 0),
            width=10,
        ),
    ]
    layer = mapsy.LineLayer(items)
    assert layer.items == items

    with assert_render_equality(tmp_path, "test_line_layer.png") as map:
        map.add_layer(layer)


def test_line_joins(tmp_path):
    s = LineString([(0, 0), (0.5, 0), (0.5, 0.5), (0, 0.2)])
    s0 = s
    s1 = transform(s, lambda x: x + 0.6)

    items = [
        mapsy.LineItem(
            geometry=s0,
            color=mapsy.Colors.RED,
            width=14,
            join=mapsy.LineJoin.ROUND,
        ),
        mapsy.LineItem(
            geometry=s1,
            color=mapsy.Colors.GREEN,
            width=14,
            join=mapsy.LineJoin.BEVEL,
        ),
    ]
    layer = mapsy.LineLayer(items)
    assert layer.items == items

    with assert_render_equality(
        tmp_path, "test_line_joins.png", box=(-0.2, -0.2, 1.2, 1.2)
    ) as map:
        map.add_layer(layer)


def test_line_caps(tmp_path):
    s = LineString([(0.2, 0), (0.4, 0)])
    s0 = s
    s1 = transform(s, lambda x: x + 0.3)
    s2 = transform(s, lambda x: x + 0.6)

    items = [
        mapsy.LineItem(
            geometry=s0,
            color=mapsy.Colors.RED,
            width=14,
            cap=mapsy.LineCap.BUTT,
        ),
        mapsy.LineItem(
            geometry=s1,
            color=mapsy.Colors.GREEN,
            width=14,
            cap=mapsy.LineCap.ROUND,
        ),
        mapsy.LineItem(
            geometry=s2,
            color=mapsy.Colors.BLUE,
            width=14,
            cap=mapsy.LineCap.SQUARE,
        ),
    ]
    layer = mapsy.LineLayer(items)
    assert layer.items == items

    with assert_render_equality(
        tmp_path, "test_line_caps.png", box=(-0.2, -0.2, 1.2, 0.8)
    ) as map:
        map.add_layer(layer)
