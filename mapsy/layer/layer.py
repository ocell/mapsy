from typing import Protocol
from abc import abstractmethod

from mapsy.render.context import RenderContext


class Layer(Protocol):
    @abstractmethod
    def render(
        self,
        renderer: RenderContext,
    ) -> None: ...
