import mapy
from shapely.geometry import Point

from test.util import assert_render_equality


def test_circle_layer(tmp_path):
    items = [
        mapy.CircleItem(
            geometry=Point(0, 0),
            color=mapy.Color(1, 0, 0),
            line_color=mapy.Color(0, 1, 0),
            line_width=4,
            radius=20,
        ),
        mapy.CircleItem(
            geometry=Point(0.5, 0.5),
            color=mapy.Color(0, 1, 0),
            line_color=mapy.Color(0, 0, 1),
            line_width=10,
            radius=30,
        ),
    ]
    layer = mapy.CircleLayer(items)
    with assert_render_equality(tmp_path, "test_circle_layer.png") as map:
        map.add_layer(layer)
