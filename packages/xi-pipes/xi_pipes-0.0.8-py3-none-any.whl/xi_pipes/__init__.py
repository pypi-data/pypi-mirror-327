"""
Custom pipes.
"""
from collections.abc import Hashable
import itertools
from math import ceil
from typing import Any, Generator, Iterable, Callable, TypeVar, Union
import functools
from itertools import tee
from pipe import Pipe

# pylint: disable=invalid-name
U = TypeVar("U")
T = TypeVar("T")
S = TypeVar("S")

@Pipe
def reduce(iterable: Iterable[T], fn: Callable[[T, T], T]) -> T:
    """
    Reduce through pipes.

    Args:
        iterable (Iterable[T]): An iterable.
        fn (Callable[[T, T], T]): A reduction function.

    Returns:
        T: The reduction result.
    """
    return functools.reduce(fn, iterable)

@Pipe
def fold(iterable: Iterable[T], fn: Callable[[S, T], S], initial:S) -> S:
    """
    Fold through pipes.

    Args:
        iterable (Iterable[T]): An iterable.
        fn (Callable[[T, T], T]): A reduction function.

    Returns:
        T: The reduction result.
    """
    return functools.reduce(fn, iterable, initial)

@Pipe
def flatten(iterable: Iterable[Iterable[T]]) -> Generator[T, None, None]:
    """
    Flatten an iterable one step in depth.

    Args:
        iterable (Iterable[T]): An iterable.

    Returns:
        Generator[T, None, None]: The flattened iterable.
    """
    return (
        y
        for x in iterable
        for y in x
    )

@Pipe
def split(
    iterable: Iterable[T],
    fn: Callable[[T], bool]
) -> tuple[list[T], list[T]]:
    """
    Split the values of an iterable in two list by the result of a deciding
    function. The elements of the iterable are sent to the first list if
    applying them in the deciding function gives a boolean True, otherwise the
    element is sent to the second list.

    Args:
        iterable (Iterable[T]): The inital iterable.
        fn (Callable[[T], bool]): A function that test each element of the
            iterable to True or False.

    Returns:
        tuple[list[T], list[T]]: A tuple of lists, of elements from the
            iterable. The first list contains the True passing elements, the
            second one the False passing elements.
    """
    positives = []
    negatives = []
    for i in iterable:
        if fn(i):
            positives.append(i)
        else:
            negatives.append(i)
    return positives, negatives

@Pipe
def flatmap(
    iterable: Iterable[Iterable[T]],
    fn: Callable[[T], S]
) -> Generator[S, None, None]:
    """
    Flattens an iterable one step deep, and then applies them to a function.
    The result is a flat iterable.

    Args:
        iterable (Iterable[Iterable[T]]): The initial iterable.
        fn (Callable[[T], S]): The function to apply the flattened values.

    Yields:
        Generator[S, None, None]: The result of apply the function to values of
            the flattened iterable.
    """
    return (
        fn(y)
        for x in iterable
        for y in x
    )

RecursiveIterable = Union[T, Iterable['RecursiveIterable']]
@Pipe
def deep_flatmap(
    iterable: RecursiveIterable,
    fn: Callable[[T], S]
) -> Generator[S, None, None]:
    """
    A flatmap version that fully flattens the iterable before apply them to the
        function.

    Args:
        iterable (RecursiveIterable): An iterable.
        fn (Callable[[T], S]): A mapping function.

    Yields:
        Generator[S, None, None]: The mapped values after fully flatten the
            iterable.
    """
    # pylint: disable=no-value-for-parameter
    if isinstance(iterable, Iterable):
        for nested in iterable:
            yield from nested | deep_flatmap(fn)
    else:
        yield fn(iterable)

@Pipe
def deep_flatten(iterable: RecursiveIterable) -> Generator[object, None, None]:
    """
    Fullu flattens an iterale.

    Args:
        iterable (RecursiveIterable): An iterable.

    Yields:
        Generator[object, None, None]: The flattened iterable.
    """
    # pylint: disable=no-value-for-parameter
    if isinstance(iterable, Iterable):
        for nested in iterable:
            yield from nested | deep_flatten()
    else:
        yield iterable

@Pipe
def as_dict(iterable: Iterable[tuple[T, S]]) -> dict[T, S]:
    """
    Converts the input iterable into a dictionary.

    Args:
        iterable (Iterable[tuple[T, S]]): An iterable of key, value tuples.

    Returns:
        dict[T, S]: The resulting dictionary.
    """
    return dict(iterable)

@Pipe
def as_list(iterable: Iterable[T]) -> list[T]:
    """
    Converts an iterable into a list.

    Args:
        iterable (Iterable[T]): An iterable.

    Returns:
        list[T]: The resulting list.
    """
    return list(iterable)

@Pipe
def as_set(iterable: Iterable[T]) -> set[T]:
    """
    Convert an iterable into a set.

    Args:
        iterable (Iterable[T]): An iterable.

    Returns:
        set[T]: The resulting set.
    """
    return set(iterable)

@Pipe
def map_on_tuples(
    iterable: Iterable[tuple[Any]],
    *fns: Callable[[Any], Any]
) -> Iterable[tuple[Any]]:
    """
    Maps tuple elements. For each element in the tuple uses
    a different mapping function.

    Args:
        iterable (Iterable[tuple[Any]]): An iterable.

    Returns:
        Iterable[tuple[Any]]: The resulting mapped iterable.
    """
    for x in iterable:
        yield tuple(fi(xi) for xi, fi in zip(x, fns))

@Pipe
def enumeration(iterable: Iterable[T]) -> Iterable[tuple[int, T]]:
    """
    Enumerates an iterable.

    Args:
        iter (Iterable[T]): An iterable.

    Yields:
        Iterable[tuple[int, T]]: An enumerated iterable.
    """
    for i, x in enumerate(iterable):
        yield i, x

@Pipe
def print_count(
    iterable: Iterable[T],
    message: str
) -> Iterable[T]:
    """
    Prints out the number of elements in the iterable.

    Args:
        iterable (Iterable[T]): An iterable.
        message (str): The text to be shown. The size of the iterable will be
            interpolated as "{size}" or f"{{size}}"

    Returns:
        Iterable[T]: The same input iterable.
    """
    it1, it2 = tee(iterable)
    print(format(message).format(size= len(list(it1))))
    yield from it2


def identical(x: T) -> T:
    """
    An identity function.

    Args:
        x (T): A value.

    Returns:
        T: The same input value untouched.
    """
    return x

HT = TypeVar("HT", bound=Hashable)
@Pipe
def remove_duplicates(
    iterable:Iterable[T],
    key:Callable[[T], HT]=identical
) -> Iterable[T]:
    """
    Removes duplicates in the iterable.

    Args:
        iterable (Iterable[T]): An Iterable.
        key (Calable[[T], HT]): A function to calculate key, the result of the
            function must be hashable value. Be default is the 'identical'
            function.

    Yields:
        Iterable[T]: An iterable without duplicated elements.
    """
    seen = set()
    for i in iterable:
        k = key(i)
        if k in seen:
            continue
        seen.add(k)
        yield i

@Pipe
def set_context(
    iterable: Iterable[T],
    context: dict[S, U],
    key:S,
    val:Callable[[Iterable[T]],U]
) -> Iterable[T]:
    """
    Assigns a value to context dictionary.

    Args:
        iterable (Iterable[T]): An iterable.
        context (dict[S, U]): A dictionary used as context for the pipeline.
        key (S): The name of the assigned value.
        val (Callable[[Iterable[T],U]]): A function to calculate the value from
            the iterable.

    Yields:
        Iterable[T]: The input iterable.
    """
    it1, it2 = tee(iterable)
    value = val(it2)
    context[key] = value
    yield from it1

@Pipe
def branch(
    iterable: Iterable[tuple[Any]],
    *fns: Callable[[Iterable],Iterable]
) -> Iterable[tuple[Any]]:
    """
    Branch an iterable of tuples.

    Each branch can be proccesed as an independent iterable.
    Values from each branch are reconverted to an iterable of tuples.
    Each branch should return the same number of elements.

    Args:
        iterable (Iterable[tuple[Any]]): An iterable of tuples.

    Returns:
        Iterable[tuple[Any]]: An Iterable of tuples.
    """
    return zip(
        *(fn(it) for it, fn in zip(zip(*iterable), fns))
    )

@Pipe
def as_chunks(
    iterable: Iterable[T],
    n_chunks: int
) -> Iterable[list[T]]:
    """
    Splits an iterable in chunks.

    Args:
        iterable (Iterable[T]): An iterable.
        n_chunks (int): The number of chunks to split the iterable.

    Returns:
        Iterable[list[T]]: An iterable of chunks.
    """
    data = iterable | as_list
    chunk_size = int(ceil(len(data) / n_chunks))
    data_iter = iter(data)
    return iter(lambda: list(itertools.islice(data_iter, chunk_size)), [])

@Pipe
def as_chunk_with_size(
    iterable: Iterable[T],
    chunk_size: int
) -> Iterable[list[T]]:
    """
    Splits an iterable in chunks.

    Args:
        iterable (Iterable[T]): An iterable.
        chunk_size (int): The size of the chunks.

    Returns:
        Iterable[list[T]]: An iterable of chunks.
    """
    data_iter = iter(iterable)
    return iter(lambda: list(itertools.islice(data_iter, chunk_size)), [])

S = TypeVar("S")
@Pipe
def invoke(
    iterable: Iterable[T],
    func: Callable[..., S],
    *args,
    **kwargs
) -> S:
    """
    Invokes a function with the iterable as first argument.

    Args:
        iterable (Iterable[T]): An iterable.
        func (Callable[..., S]): A function to invoke.
        *args: Additional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        S: The result of the function invocation.
    """
    return func(iterable, *args, **kwargs)

@Pipe
def foreach(
    iterable: Iterable[T],
    func: Callable[[T], None],
    *args,
    **kwargs
) -> None:
    """
    Applies a function to each element of the iterable.

    Args:
        iterable (Iterable[T]): An iterable.
        func (Callable[[T], None]): A function to apply.
        *args: Additional arguments.
        **kwargs: Additional keyword arguments.
    """
    for x in iterable:
        func(x, *args, **kwargs)

@Pipe
def sliding_window(
    iterable: Iterable[T],
    size: int,
    step: int = 1
) -> Iterable[list[T]]:
    """
    Sliding window over an iterable.

    Args:
        iterable (Iterable[T]): An iterable.
        size (int): The size of the window.
        step (int, optional): The step size. Defaults to 1.

    Returns:
        Iterable[list[T]]: An iterable of windows.
    """
    it = iter(iterable)
    window = list(itertools.islice(it, size))
    while len(window) == size:
        yield window
        window = window[step:] + list(itertools.islice(it, step))

@Pipe
def map_update(
    iterable: Iterable[T],
    func: Callable[[T], None],
    *args,
    **kwargs
) -> Iterable[T]:
    """
    Updates the elements of the iterable using a function.

    Args:
        iterable (Iterable[T]): An iterable.
        func (Callable[[T]], None): A function to update the elements.

    Returns:
        Iterable[T]: An iterable of updated elements.
    """
    for x in iterable:
        func(x, *args, **kwargs)
        yield x