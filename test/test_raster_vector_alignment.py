import mapsy
from mock import Mock
from shapely.geometry import Point

from test.util import assert_render_equality

STATUE_OF_LIBERTY = Point(-74.0445, 40.6892)
# Carto Positron z16/19288/24645; © OpenStreetMap contributors © CARTO.
STATUE_TILE_BOUNDS = (
    -74.0478515625,
    40.68896903762434,
    -74.0423583984375,
    40.69313415330808,
)


def test_statue_of_liberty_raster_point_alignment(tmp_path):
    mock_client = Mock()
    with open("test/data/statue_of_liberty_tile.png", "rb") as file:
        mock_client.get_tile.return_value = file.read()

    raster = mapsy.TiledRasterLayer(
        sources=["fixture"],
        min_zoom=16,
        max_zoom=16,
        tile_size=256,
        client=mock_client,
    )
    marker = mapsy.CircleLayer(
        [
            mapsy.CircleItem(
                geometry=STATUE_OF_LIBERTY,
                color=mapsy.Color(1, 1, 0, 0.9),
                radius=6,
                line_color=mapsy.Colors.BLACK,
                line_width=2,
            )
        ]
    )

    with assert_render_equality(
        tmp_path,
        "test_statue_of_liberty_alignment.png",
        size=(256, 256),
        box=STATUE_TILE_BOUNDS,
    ) as map:
        map.add_layer(raster)
        map.add_layer(marker)

    mock_client.get_tile.assert_called_once_with("fixture", 16, 19288, 24645)
