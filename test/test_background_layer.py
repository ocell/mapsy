import mapy

from test.util import assert_render_equality


def test_fill_layer(tmp_path):
    with assert_render_equality(tmp_path, "test_background_layer.png") as map:
        map.add_layer(mapy.BackgroundLayer(color=mapy.Colors.MAGENTA))
