import mapsy
from test.util import assert_render_equality


def test_annotation(tmp_path):
    attribution = mapsy.Attribution("This is a test :)")

    with assert_render_equality(tmp_path, "test_attribution.png") as map:
        map.add_layer(attribution)
