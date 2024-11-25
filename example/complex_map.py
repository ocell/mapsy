import json
from typing import Any

import mapy
from shapely.geometry import shape, Polygon

import random
from mapy.geo_util import Box, merge_bounds


def load_geojson(file_path: str) -> tuple[list[Polygon], dict[str, Any]]:
    with open(file_path, "r") as f:
        data = json.load(f)
    features = data["features"]
    geoms = []
    properties = []
    for feature in features:
        geom = shape(feature["geometry"])
        properties.append(feature["properties"])
        geoms.append(geom)
    return geoms, properties


def build_fill_items(polygons: list[Polygon]) -> list[mapy.FillItem]:
    items = []
    for poly in polygons:
        fill_color = mapy.Color.from_hsv(random.random(), 0.7, 0.5, 0.2)
        line_color = mapy.Color(0, 0, 0, 0.6)
        line_width = 1
        items.append(mapy.FillItem(poly, fill_color, line_color, line_width))
    return items


def build_symbol_items(
    polygons: list[Polygon], properties: list[dict[str, Any]]
) -> list[mapy.SymbolItem]:
    items = []
    for poly, props in zip(polygons, properties):
        poly.centroid
        text = props["NAME_2"]
        symbol_item = mapy.SymbolItem(
            poly.centroid,
            text=text,
            text_weight=mapy.FontWeight.BOLD,
            text_size=18,
            text_color=mapy.Colors.BLACK,
            text_outline_color=mapy.Colors.WHITE,
            text_outline_width=2,
            text_anchor=mapy.TextAnchor.CENTER,
            text_offset=(0, 40) if text == "Brandenburg" else (0, 0),
        )
        items.append(symbol_item)
    return items


def main():
    map = mapy.Map()
    random.seed(0)
    geoms, properties = load_geojson("example/districts_germany.json")
    bboxes = [Box(*geom.bounds) for geom in geoms]
    bbox = merge_bounds(bboxes).with_relative_padding(0.05)

    tile_layer = mapy.TiledRasterLayer(
        [
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        ]
    )

    map.add_layer(tile_layer)
    map.add_layer(mapy.FillLayer(build_fill_items(geoms)))
    map.add_layer(mapy.SymbolLayer(build_symbol_items(geoms, properties)))
    map.add_layer(mapy.Attribution("© OpenStreetMap contributors"))

    render_mode = mapy.FixedScreenSize(bbox, mapy.ScreenSize(1400, 1175))
    map.render(render_mode).write_to_png("images/EnforcedScreenSize.png")
    render_mode = mapy.FixedBBox(bbox, 1000**2)
    map.render(render_mode).write_to_png("images/EnforcedBBox.png")


if __name__ == "__main__":
    main()
