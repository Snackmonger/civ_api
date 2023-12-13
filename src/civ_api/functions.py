from random import choice, randint
from enum import StrEnum

from .constants.resources import resource_minmax
from .type_aliasing import BasicDict, ResourceRanges


class Abstraction: pass


def test_get_random_resources(resource_ranges: ResourceRanges | None = None
                              ) -> dict[str, int]:
    '''
    Get a random assortment of the given resources.
    '''
    if resource_ranges is None:
        resource_ranges = resource_minmax

    number_of_resources = randint(1, 4)
    resources: dict[str, int] = {}
    for _ in range(number_of_resources):
        res = choice(list(resource_ranges))
        while res in resources:
            res = choice(list(resource_ranges))

        val = choice(resource_ranges[res])
        val = choice(range(1, val + 1))
        resources.update({res:val})

    return resources


def total_resources(resources: list[BasicDict]) -> dict[str, int]:
    total: dict[str, int] = {}
    for resource in resources:
        for k, v in resource.items():
            if not isinstance(v, int):
                continue
            if k not in total:
                total.update({k: v})
            else:
                total.update({k: total[k] + v})
    return total


def vals(enum: type[StrEnum]) -> list[str]:
    '''Syntactic shortcut to get the values of a string enum.'''
    return [e.value for e in enum]


def SQL_keyrefs_insert(dictionary: BasicDict) -> tuple[str, str]:
    '''
    {"key": value, "key2": value} -> ("key1, key2", ":key1, :key2")
    '''
    dictionary_ = SQL_keyrefs_dict(dictionary)
    keys = ", ".join(dictionary_.keys())
    references = ', '.join(dictionary_.values())
    return (keys, references)


def SQL_keyrefs_dict(dictionary: BasicDict) -> dict[str, str]:
    """
    {"key": value, "key2": value} -> {"key": ":key", "key2": ":key2"}
    """
    dictionary_: dict[str, str] = {}
    for k in dictionary:
        dictionary_.update({k:":"+k})
    return dictionary_


def SQL_keyrefs_eq(dictionary: BasicDict) -> list[str]:
    """
    {"key": value, "key2": value} -> ["key = :key", "key2 = :key2"]
    """
    dictionary_ = SQL_keyrefs_dict(dictionary)
    return [str(k + " = " + v) for k, v in dictionary_.items()]
