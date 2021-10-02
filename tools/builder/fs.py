
import os

from typing import Iterator
from contextlib import contextmanager


@contextmanager
def pushd(directory: str) -> Iterator[str]:
    """A with-context that encapsulates pushd/popd."""
    cwd = os.getcwd()
    os.chdir(directory)
    try:
        yield directory
    finally:
        os.chdir(cwd)
