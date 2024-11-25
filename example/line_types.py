import mapy
from shapely import LineString
from shapely import affinity

from mapy.color import Color, Colors
from mapy.common import LineCap, LineJoin


def simple_line(y_offset: int = 0, x_offset: int = 0) -> LineString:
    return affinity.translate(
        LineString([(1, 1), (2, 1), (2, 2), (2.5, 1), (2.6, 1.1)]),
        xoff=x_offset * 2,
        yoff=y_offset * 1.7,
    )


def make_line_variants():
    map = mapy.Map()
    lines = []
    texts = []

    def add_items(
        geometry: LineString, color: Color, cap: LineCap = None, join: LineJoin = None
    ):
        cap_to_set = cap if cap is not None else LineCap.BUTT
        join_to_set = join if join is not None else LineJoin.MITER
        text = f"CAP {cap.value}" if cap else f"JOIN {join.value}"
        lines.append(
            mapy.LineItem(
                geometry=geometry,
                color=color,
                cap=cap_to_set,
                join=join_to_set,
                width=12,
                outline_width=3,
                outline_color=Colors.BLACK,
            )
        )
        texts.append(
            mapy.SymbolItem(
                text=text,
                geometry=affinity.translate(geometry.centroid, xoff=-1),
                text_color=Colors.BLACK,
                text_size=14,
                text_font="times",
                text_weight=mapy.FontWeight.BOLD,
                text_slant=mapy.FontSlant.NORMAL,
            )
        )

    total_lines = len(LineCap) + len(LineJoin)
    geometries = [simple_line(n % 3, int(n > 2)) for n in range(total_lines)]

    for n, cap in enumerate(LineCap):
        line = geometries[n]
        add_items(line, Colors.GRAY, cap=cap)

    for n, join in enumerate(LineJoin, len(LineCap)):
        line = geometries[n]
        add_items(line, Colors.GRAY, join=join)

    bounds = mapy.bounds_for_geometries(geometries)
    map.add_layer(mapy.BackgroundLayer(Colors.WHITE))
    map.add_layer(mapy.LineLayer(lines))
    map.add_layer(mapy.SymbolLayer(texts))

    map.render(
        mapy.FixedBBox(bounds.with_relative_padding(0.12), 400 * 400)
    ).write_to_png("images/line_types.png")


if __name__ == "__main__":
    make_line_variants()
