from typing import Any, Callable, Iterator, List, Union
from dyncfg import ConfigValue


class ConfigValueList:
    """
    A wrapper for a list of ConfigValue objects that supports method chaining.
    This stub provides type hints for intellisense and static analysis.
    """

    values: List[ConfigValue]

    def __init__(self, values: List[ConfigValue]) -> None: ...

    def __iter__(self) -> Iterator[ConfigValue]: ...

    def __getitem__(self, index: Union[int, slice]) -> Union[ConfigValue, List[ConfigValue]]: ...

    def __repr__(self) -> str: ...

    def __getattr__(self, name: str) -> Callable[..., Union["ConfigValueList", List[Any]]]: ...
