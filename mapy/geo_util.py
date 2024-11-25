from functools import reduce
import math
from typing import NamedTuple
import affine
import pyproj
from shapely import MultiLineString, MultiPolygon, LineString, Point, Polygon
from shapely.ops import transform
from shapely import transform as transform_numpy
from shapely.geometry.base import BaseGeometry
import mercantile


class Box(NamedTuple):
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def to_xy(self):
        x0, y0 = mercantile.xy(self.x_min, self.y_min)
        x1, y1 = mercantile.xy(self.x_max, self.y_max)
        return Box(x0, y0, x1, y1)

    @staticmethod
    def from_lng_lat(lng_min, lat_min, lng_max, lat_max):
        return Box(x_min=lng_min, y_min=lat_min, x_max=lng_max, y_max=lat_max)

    def to_lng_lat(self):
        lon0, lat0 = mercantile.lnglat(self.x_min, self.y_min)
        lon1, lat1 = mercantile.lnglat(self.x_max, self.y_max)
        return Box(lon0, lat0, lon1, lat1)

    def merge(self, other: "Box"):
        return Box(
            min(self.x_min, other.x_min),
            min(self.y_min, other.y_min),
            max(self.x_max, other.x_max),
            max(self.y_max, other.y_max),
        )

    def with_padding(self, padding: float):
        dx = self.delta_x * padding
        dy = self.delta_y * padding
        return Box(
            self.x_min - dx,
            self.y_min - dy,
            self.x_max + dx,
            self.y_max + dy,
        )

    def with_relative_padding(self, padding: float):
        """Padding is relative to the size of the bounding box.

        padding = 0.1 means that the padding will be 10% of the size of the
        bounding box per side.
        """
        average_delta = (self.delta_x + self.delta_y) / 2
        dx = average_delta * padding
        dy = average_delta * padding
        return Box(
            self.x_min - dx,
            self.y_min - dy,
            self.x_max + dx,
            self.y_max + dy,
        )

    def with_new_aspect_ratio_as_padding(self, aspect_ratio: float):
        if self.aspect_ratio > aspect_ratio:
            dx = self.delta_x
            dy = dx / aspect_ratio
        else:
            dy = self.delta_y
            dx = dy * aspect_ratio

        center_x, center_y = self.center

        return Box(
            center_x - dx / 2,
            center_y - dy / 2,
            center_x + dx / 2,
            center_y + dy / 2,
        )

    @property
    def delta_x(self):
        return self.x_max - self.x_min

    @property
    def delta_y(self):
        return self.y_max - self.y_min

    @property
    def center(self):
        return (self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2

    @property
    def aspect_ratio(self):
        return self.delta_x / self.delta_y


def merge_bounds(bounds: list[Box]) -> Box:
    return reduce(lambda a, b: a.merge(b), bounds)


def bounds_for_geometries(geometries: list[BaseGeometry]) -> Box:
    bounds = [Box(*geom.bounds) for geom in geometries]
    return merge_bounds(bounds)


def bbox_to_affine(
    bbox: Box[float, float, float, float],
    shape: tuple[int, int],
) -> affine.Affine:
    scale_x = bbox.delta_x / shape[0]
    scale_y = bbox.delta_y / shape[1]
    return affine.Affine(scale_x, -1, bbox.x_min, -1, -scale_y, bbox.y_max)


def wgs84_to_web_mercator(geom: BaseGeometry):
    wgs84 = pyproj.CRS("EPSG:4326")
    epsg_3857 = pyproj.CRS("EPSG:3857")
    project = pyproj.Transformer.from_crs(wgs84, epsg_3857, always_xy=True).transform
    return transform(project, geom)


class Transformer:
    def __init__(self, bbox: Box, shape: tuple[int, int]):
        self.bbox = Box(*bbox)
        self.shape = shape
        self.project = pyproj.Transformer.from_crs(
            pyproj.CRS("EPSG:4326"), pyproj.CRS("EPSG:3857"), always_xy=True
        ).transform
        bbox_xy = self.bbox.to_xy()
        self.image_to_global_crs = bbox_to_affine(bbox_xy, self.shape)
        self.global_to_image_crs = ~self.image_to_global_crs

    def transform_to_image_crs(self, geom: BaseGeometry):
        geom = transform(self.project, geom)

        return affine_to_local_crs(geom, self.global_to_image_crs)


def affine_to_local_crs(polygon: BaseGeometry, affine: affine.Affine) -> BaseGeometry:
    def project(coord_list):
        result = coord_list.copy()
        for i, coord in enumerate(coord_list):
            result[i] = affine * coord
        return result

    return transform_numpy(polygon, project)


def any_polygon_to_lines(polygon: Polygon | MultiPolygon):
    def polygon_to_lines(polygon: Polygon):
        return [
            LineString(polygon.exterior.coords),
            *[LineString(ring.coords) for ring in polygon.interiors],
        ]

    if isinstance(polygon, MultiPolygon):
        return [line for g in polygon.geoms for line in polygon_to_lines(g)]
    return polygon_to_lines(polygon)


def any_line_to_points(line: MultiLineString | LineString):
    def line_to_points(line: LineString):
        return [Point(coords) for coords in line.coords]

    if isinstance(line, MultiLineString):
        return [point for line in line.geoms for point in line_to_points(line)]
    return line_to_points(line)


def any_polygon_to_points(polygon: Polygon | MultiPolygon):
    lines = any_polygon_to_lines(polygon)
    return [point for line in lines for point in any_line_to_points(line)]


def zoomForBounds(bbox: Box, shape: tuple[int, int]):
    ry1 = math.log(
        (math.sin(math.radians(bbox.y_min)) + 1) / math.cos(math.radians(bbox.y_min))
    )
    ry2 = math.log(
        (math.sin(math.radians(bbox.y_max)) + 1) / math.cos(math.radians(bbox.y_max))
    )
    ryc = (ry1 + ry2) / 2
    centerY = math.degrees(math.atan(math.sinh(ryc)))

    resolutionHorizontal = bbox.delta_x / shape[0]

    vy0 = math.log(math.tan(math.pi * (0.25 + centerY / 360)))
    vy1 = math.log(math.tan(math.pi * (0.25 + bbox.y_max / 360)))
    viewHeightHalf = shape[1] / 2.0
    zoomFactorPowered = viewHeightHalf / (40.7436654315252 * (vy1 - vy0))
    resolutionVertical = 360.0 / (zoomFactorPowered * 256)

    resolution = max(resolutionHorizontal, resolutionVertical)

    return math.log(360 / (resolution * 256), 2)
