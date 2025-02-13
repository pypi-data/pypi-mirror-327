# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# %%
from abc import ABC
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic, Union

T = TypeVar("T")
S = TypeVar("S")

class Result(ABC, Generic[T, S]):
  def is_ok(self) -> bool:
    return isinstance(self, Ok)
  def is_err(self) -> bool:
    return isinstance(self, Error)
  def map(self, func: Callable):
    if isinstance(self, Ok):
      return Ok(func(self.value))
    return self
  def flat_map(self, func: Callable):
    return func(self)
  def unwrap(self) -> Union[T, S]:
    if isinstance(self, Ok):
      return self.unwrap()
    if isinstance(self, Error):
      return self.unwrap()
    raise ValueError("Result is neither Ok nor Error")
  def unwrap_or(self, default: S) -> S:
    if isinstance(self, Ok):
      return self.unwrap()
    return default

@dataclass
class Error(Result, Generic[T]):
  def __init__(self, err: T):
    self.err = err
  def unwrap(self) -> T:
    return self.err

@dataclass
class Ok(Result, Generic[S]):
  def __init__(self, value: S):
    self.value = value
  def unwrap(self) -> S:
    return self.value


def with_error(func:Callable[..., S]) -> Callable[..., Result[S, str]]:
  def wrapper(*args, **kwargs):
    try:
      result = func(*args, **kwargs)
    except Exception as exception:
      return Error(str(exception))
    return Ok(result)
  return wrapper


@with_error
def divide(a: int, b: int) -> float:
  return a / b


a = divide(1, 0).map(lambda x: x*2)
print(a)