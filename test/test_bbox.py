import pytest
from mapy.geo_util import Box


def test_bbox_round_trip():
    bbox = Box(1, 2, 3, 4)
    bbox_round_trip = bbox.to_xy().to_lng_lat()

    assert bbox == pytest.approx(bbox_round_trip)


def test_bbox_merge():
    bbox1 = Box(1, 2, 3, 4)
    bbox2 = Box(2, 3, 7, 8)

    merged = bbox1.merge(bbox2)

    assert merged == Box(1, 2, 7, 8)


def test_bbox_padding():
    bbox = Box(1, 2, 3, 4)
    padded = bbox.with_relative_padding(0.1)

    assert padded == pytest.approx(Box(0.8, 1.8, 3.2, 4.2))


def test_bbox_aspect_ratio_padding():
    bbox = Box(1, 2, 3, 4)
    padded = bbox.with_new_aspect_ratio_as_padding(2)

    assert padded.aspect_ratio == 2
    assert padded == pytest.approx(Box(0, 2, 4, 4))
