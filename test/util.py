import pytest
import mapy
from contextlib import contextmanager
from os import path


@contextmanager
def assert_render_equality(
    tmp_path: str,
    filename: str,
    create_input: bool = False,
    size=(100, 100),
    box=(0, 0, 1, 1),
):
    map = mapy.Map()
    yield map

    input_path = path.join("test", "data", filename)
    output_path = input_path if create_input else path.join(tmp_path, filename)
    surf = map.render(
        mapy.FixedScreenSize(
            mapy.Box(*box),
            mapy.ScreenSize(*size),
        )
    )
    surf.write_to_png(output_path)
    assert path.exists(output_path)
    with open(output_path, "rb") as f:
        with open(input_path, "rb") as f_ref:
            assert f.read() == f_ref.read()
