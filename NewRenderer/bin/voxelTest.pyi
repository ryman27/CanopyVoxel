# voxelTest.pyi

from typing import Any


class coordinate:
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int) -> None: ...

    def __repr__(self) -> str: ...


class hsv:
    h: float
    s: float
    v: float

    def __init__(self, hue: float, saturation: float, value: float) -> None: ...

    def __repr__(self) -> str: ...


class rgb:
    red: float
    g: float
    b: float

    def __init__(self, red: float, green: float, blue: float) -> None: ...

    def __repr__(self) -> str: ...


class rgba:
    red: float
    g: float
    b: float
    a: float

    def __init__(self, red: float, green: float, blue: float, alpha: float) -> None: ...

    def __repr__(self) -> str: ...


class voxelWindow:
    def __init__(self, world_length: int, chunk_length: int, window_width: int, window_height: int,
                 background_color: rgba) -> None: ...

    def GetVoxel(self, world_pos: coordinate) -> rgba: ...

    def SetVoxel(self, world_pos: coordinate, color: rgba) -> None: ...

    def ShouldClose(self) -> bool: ...
