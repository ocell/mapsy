from functools import reduce
import math
import os
import tempfile
from hashlib import md5

import mercantile
from mercantile import LngLatBbox, Tile
from requests import get

from mapy.common import ImageFilter, MapyInfo
from mapy.geo_util import Box, bbox_to_affine, zoomForBounds
from mapy.layer.layer import Layer
from mapy.render.context import RenderContext


class TileClient:
    def __init__(self, cache_dir: str | None) -> None:
        self.cache_dir = cache_dir
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)

    def get_tile(self, url: str, z: int, x: int, y: int) -> bytes:
        cache_path = None
        if self.cache_dir:
            hashed = md5(url.encode()).hexdigest()
            cache_path = os.path.join(self.cache_dir, hashed, str(z), str(x), str(y))
            if os.path.exists(cache_path):
                with open(cache_path, "rb") as fp:
                    return fp.read()

        hydrated_url = url.format(z=z, x=x, y=y)

        response = get(
            hydrated_url,
            headers={"User-Agent": f"{MapyInfo.AGENT_NAME}/{MapyInfo.VERSION}"},
        )
        if response.status_code == 200:
            if cache_path:
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                with open(cache_path, "wb") as fp:
                    fp.write(response.content)
            return response.content
        else:
            raise FileNotFoundError


class TiledRasterLayer(Layer):
    def __init__(
        self,
        sources: list[str],
        min_zoom: int = 0,
        max_zoom: int = 18,
        tile_size: int = 256,
        client: TileClient = None,
        use_cache: bool = True,
    ) -> None:
        self.tile_sources = sources
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.tile_size = tile_size
        cache_dir = tempfile.gettempdir() if use_cache else None
        self.client = client or TileClient(cache_dir)

    def render(
        self,
        context: RenderContext,
    ) -> None:
        tiles = self.get_tiles(context.screen_size, context.bbox)

        output_to_world = context.transformer.image_to_global_crs

        x_0_tiles = tiles[0].x
        y_0_tiles = tiles[0].y

        images = []
        coords = []
        bounds: list[Box] = []

        for tile in tiles:
            x_offset = (tile.x - x_0_tiles) * self.tile_size
            y_offset = (tile.y - y_0_tiles) * self.tile_size
            coords.append((x_offset, y_offset))
            images.append(self.get_image(tile))
            bounds.append(Box(*mercantile.xy_bounds(tile)))

        x_count = max(tile.x for tile in tiles) - min(tile.x for tile in tiles) + 1
        y_count = max(tile.y for tile in tiles) - min(tile.y for tile in tiles) + 1

        combined_tile_size = (self.tile_size * x_count, self.tile_size * y_count)
        combined_surface = context.render_backend.combine_images(
            images, coords, combined_tile_size
        )
        combined_bbox = reduce(lambda a, b: a.merge(b), bounds)

        tile_to_world = bbox_to_affine(combined_bbox, combined_tile_size)

        surface_to_output = ~output_to_world * tile_to_world
        context.render_backend.draw_image(
            combined_surface, surface_to_output, image_filter=ImageFilter.BEST
        )

    def get_image(self, tile: Tile) -> bytes:
        for source in self.tile_sources:
            try:
                return self.client.get_tile(source, tile.z, tile.x, tile.y)
            except FileNotFoundError:
                continue
        raise FileNotFoundError

    def get_tiles(self, image_shape, bbox: LngLatBbox):
        zoom_exact = zoomForBounds(bbox, image_shape)

        # we want to downscale rather than upscale -> ceil
        zoom = min(self.max_zoom, math.ceil(zoom_exact))

        tiles = list(mercantile.tiles(*bbox, zooms=[zoom]))
        return tiles
