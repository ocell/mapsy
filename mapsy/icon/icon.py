from dataclasses import dataclass
from pathlib import Path

from mapsy.common import IconAlign


@dataclass
class Icon:
    data: bytes
    size: tuple[int, int]
    alignment: IconAlign = IconAlign.CENTER

    @staticmethod
    def from_path(
        path: str,
        size: tuple[int, int],
        alignment: IconAlign = IconAlign.CENTER,
    ) -> "Icon":
        with open(path, "rb") as fp:
            data = fp.read()
        return Icon(data=data, size=size, alignment=alignment)


def _path_for_name(name: str) -> str:
    return str(Path(__file__).parent.absolute() / "data" / f"{name}.png")


def size_to_offset(size: tuple[int, int]) -> tuple[float, float]:
    return -size[0] / 2, -size[1]


class Icons:
    PIN_24 = Icon.from_path(
        path=_path_for_name("pin-24"),
        size=(24, 24),
        alignment=IconAlign.BOTTOM_CENTER,
    )
    PIN_48 = Icon.from_path(
        path=_path_for_name("pin-48"),
        size=(48, 48),
        alignment=IconAlign.BOTTOM_CENTER,
    )
