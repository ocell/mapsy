import json
from typing import Any

import mapsy
from shapely.geometry import shape, Polygon

import random
from mapsy.geo_util import Box, merge_bounds


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


def build_fill_items(polygons: list[Polygon]) -> list[mapsy.FillItem]:
    items = []
    for poly in polygons:
        fill_color = mapsy.Color.from_hsv(random.random(), 0.7, 0.5, 0.2)
        line_color = mapsy.Color(0, 0, 0, 0.6)
        line_width = 1
        items.append(mapsy.FillItem(poly, fill_color, line_color, line_width))
    return items


def build_symbol_items(
    polygons: list[Polygon], properties: list[dict[str, Any]]
) -> list[mapsy.SymbolItem]:
    items = []
    for poly, props in zip(polygons, properties):
        poly.centroid
        text = props["NAME_2"]
        symbol_item = mapsy.SymbolItem(
            poly.centroid,
            text=text,
            text_weight=mapsy.FontWeight.BOLD,
            text_size=18,
            text_color=mapsy.Colors.BLACK,
            text_outline_color=mapsy.Colors.WHITE,
            text_outline_width=2,
            text_anchor=mapsy.TextAnchor.CENTER,
            text_offset=(0, 40) if text == "Brandenburg" else (0, 0),
        )
        items.append(symbol_item)
    return items


def main():
    map = mapsy.Map()
    random.seed(0)
    geoms, properties = load_geojson("example/districts_germany.json")
    bboxes = [Box(*geom.bounds) for geom in geoms]
    bbox = merge_bounds(bboxes).with_relative_padding(0.05)

    tile_layer = mapsy.TiledRasterLayer(
        [
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        ]
    )

    map.add_layer(tile_layer)
    map.add_layer(mapsy.FillLayer(build_fill_items(geoms)))
    map.add_layer(mapsy.SymbolLayer(build_symbol_items(geoms, properties)))
    map.add_layer(mapsy.Attribution("© OpenStreetMap contributors"))

    render_mode = mapsy.FixedScreenSize(bbox, mapsy.ScreenSize(1400, 1175))
    map.render(render_mode).write_to_png("images/EnforcedScreenSize.png")
    render_mode = mapsy.FixedBBox(bbox, 1000**2)
    map.render(render_mode).write_to_png("images/EnforcedBBox.png")


if __name__ == "__main__":
    main()
