import mapy
from mock import Mock
from test.util import assert_render_equality


def test_tiled_raster_layer(tmp_path):
    mock_client = Mock()
    with open("test/data/tile.png", "rb") as f:
        tile_data = f.read()
    mock_client.get_tile.return_value = tile_data
    layer = mapy.TiledRasterLayer(sources="Test", client=mock_client)

    with assert_render_equality(tmp_path, "test_tiled_raster_layer.png") as map:
        map.add_layer(layer)
