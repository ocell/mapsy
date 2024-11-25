import mapy
from shapely import Polygon

from test.util import assert_render_equality


def test_fill_layer(tmp_path):
    items = [
        mapy.FillItem(
            polygon=Polygon([(0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)]),
            fill_color=mapy.Color(1, 0, 0),
            line_color=mapy.Color(0, 0, 0),
            line_width=1,
        ),
        mapy.FillItem(
            polygon=Polygon([(0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)]),
            fill_color=mapy.Color(0, 1, 0),
            line_color=mapy.Color(1, 1, 1),
            line_width=10,
        ),
    ]
    layer = mapy.FillLayer(items)
    assert layer.items == items

    with assert_render_equality(tmp_path, "test_fill_layer.png") as map:
        map.add_layer(layer)
