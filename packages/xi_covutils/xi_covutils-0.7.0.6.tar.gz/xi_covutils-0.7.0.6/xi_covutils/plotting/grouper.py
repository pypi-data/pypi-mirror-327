"""
Gropups ticks to be shown as groups
"""

from abc import abstractmethod
from collections import defaultdict
from functools import reduce
from typing_extensions import Protocol


class ElementGrouper(Protocol):
  """
  A base class for Element Groupers
  """
  groups: list[int]
  def __init__(self, groups: list[int]):
    self.groups = groups
  @abstractmethod
  def get_element_positions(self) -> list[float]:
    """
    Returns the positions of each element in the groups.
    """
  @abstractmethod
  def get_group_positions(self) -> list[float]:
    """
    Get the positions of each group.
    """


class ElementGrouperNull(ElementGrouper):
  """
  A simple grouper that does not group ticks.
  """
  def __init__(self, groups: list[int]):
    self.groups = groups
  def get_group_positions(self):
    return list(range(sum(self.groups)))
  def get_element_positions(self):
    return list(range(sum(self.groups)))


class ElementGrouperSimple(ElementGrouper):
  """
  A simple grouper that groups elements controlling the space between
  elements in the same group.
  """
  def __init__(self, groups: list[int], shrinking: float=0.2):
    self.groups = groups
    self.shrinking = shrinking
  def get_element_positions(self) -> list[float]:
    corrected_width = 1 - self.shrinking
    offsets = reduce(lambda x, y: x + [x[-1] + y], self.groups, [0])[:-1]
    mid_points = [(n-1)/2 for n in self.groups]
    shrinks = [
      [corrected_width * i - corrected_width * ((j-1)/2) for i in range(j)]
      for j in self.groups
    ]
    results = [
      o + m + s
      for o, m, ss in zip(offsets, mid_points, shrinks)
      for s in ss
    ]
    return results
  def get_group_positions(self) -> list[float]:
    offsets = reduce(lambda x, y: x + [x[-1] + y], self.groups, [0])[:-1]
    mid_points = [(n-1)/2 for n in self.groups]
    results = [
      o + m
      for o, m in zip(offsets, mid_points)
    ]
    return results


class ElementGrouperWithSpacers(ElementGrouper):
  """
  A simple grouper that groups elements controlling the space between
  elements in the same group and the space between groups.
  """
  def __init__(
    self,
    groups: list[int],
    internal_spacer: float=0.2,
    group_spacer: float=0.5
  ):
    self.groups = groups
    self.internal_spacer = internal_spacer
    self.group_spacer = group_spacer
  def get_element_positions(self) -> list[float]:
    results:list[float] = [0]
    acc:float =0.0
    for group in self.groups:
      for _ in range(group-1):
        acc += self.internal_spacer
        results.append(acc)
      acc += self.group_spacer
      results.append(acc)
    return results[:-1]
  def get_group_positions(self) -> list[float]:
    pos = self.get_element_positions()
    group_index = [
      i
      for i, p in enumerate(self.groups)
      for _ in range(p)
    ]
    results = defaultdict(list)
    for c_pos, index in zip(pos, group_index):
      results[index].append(c_pos)
    results = [
      sum(results[k])/len(results[k])
      for k in sorted(results.keys())
    ]
    return results
