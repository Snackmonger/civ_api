from typing import Mapping, MutableMapping


IntPair = tuple[int, int]
Coords = IntPair
ImmutableType = int | float | str | bool | None
BasicDict = MutableMapping[str, ImmutableType]
ResourceRanges = MutableMapping[str, IntPair]
