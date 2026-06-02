from __future__ import annotations

from typing import Any, Dict, Optional

JsonObject = Dict[str, Any]


class MixfontError(Exception):
    pass


class MixfontAPIError(MixfontError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        body: Optional[JsonObject] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body or {}


class MixfontGenerationError(MixfontError):
    def __init__(self, message: str, *, generation: JsonObject) -> None:
        super().__init__(message)
        self.generation = generation


class MixfontGenerationCancelledError(MixfontGenerationError):
    pass


class MixfontTimeoutError(MixfontError):
    def __init__(
        self,
        message: str,
        *,
        generation: Optional[JsonObject] = None,
    ) -> None:
        super().__init__(message)
        self.generation = generation
