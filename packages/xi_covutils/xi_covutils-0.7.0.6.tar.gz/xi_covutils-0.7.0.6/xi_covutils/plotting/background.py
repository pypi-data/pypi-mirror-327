"""
Background themes
"""
from abc import ABC
import itertools
import random
from typing import cast

from matplotlib.transforms import Affine2D, Bbox
from matplotlib import patches
from matplotlib.axes import Axes
from matplotlib.figure import Figure


# pylint: disable=too-few-public-methods
class BackgroundTheme(ABC):
  """
  Base class for background themes.
  """
  def draw_background(self, axes: Axes):
    """
    Draw the background on the axes.

    Args:
      ax (Axes): The axes to draw the background on.
    """


class LightColorSquaredBackground(BackgroundTheme):
  """
  A background that draws a tiled pattern of light colored squares.
  """
  def __init__(
    self,
    n_boxes:int=20,
    intensity:float=0.20,
    color:str="lightgray"
  ):
    self.n_boxes = n_boxes
    self.intensity = intensity
    self.color = color
    self.zorder = -1

  def set_zorder(self, zorder:int):
    """
    Set the zorder of the background.
    """
    self.zorder = zorder

  def _get_alpha(self) -> float:
    return self.intensity

  def draw_background(self, axes: Axes):
    box_width = 1/self.n_boxes
    spacer = min(box_width/self.n_boxes, box_width/10)
    for i, j in itertools.product(range(self.n_boxes), range(self.n_boxes)):
      c_alpha = self._get_alpha()
      axes.add_patch(
        patches.Rectangle(
          (i*box_width+spacer, j*box_width+spacer),
          box_width-2*spacer, box_width-2*spacer,
          edgecolor=None, facecolor=self.color,
          alpha=c_alpha, transform = axes.transAxes,
          zorder=-self.zorder
        ),
      )


class RandomLightColorSquaredBackground(LightColorSquaredBackground):
  """
  A background that draws a tiled pattern of light colored squares with random
  intensities.
  """
  def __init__(
    self,
    n_boxes:int=20,
    intensity:float=0.2,
    color:str="lightgray",
    randomness:float=0.20
  ):
    super().__init__(n_boxes, intensity, color)
    self.randomness = randomness
    self.seed = 100

  def _get_alpha(self) -> float:
    return self.intensity + (0.5 - random.random()) * self.randomness

  def draw_background(self, axes: Axes):
    random.seed(self.seed)
    return super().draw_background(axes)


class GridBackground(BackgroundTheme):
  """
  A Grid Background
  """
  def __init__(
    self,
    grids: int = 10,
    color: str = "lightgray",
    background: str = "white"
  ):
    self.grids = grids
    self.color = color
    self.background = background

  def draw_background(self, axes: Axes):
    fig = cast(Figure, axes.figure)
    trans = Affine2D().scale(fig.dpi)
    bbox = axes.get_window_extent().transformed(trans.inverted())
    bbox = cast(Bbox, bbox)
    x_diff = bbox.width
    y_diff = bbox.height
    xy_ratio = x_diff / y_diff
    grid_size = 1 / self.grids
    i = grid_size/2
    while i < 1:
      axes.axvline(i, color=self.color, zorder=-1)
      i += grid_size
    i = grid_size * xy_ratio / 2
    while i < 1:
      axes.axhline(i, color=self.color, zorder=-1)
      i += grid_size * xy_ratio


class SubGridsBackground(BackgroundTheme):
  """
  A Grid Background
  """
  # pylint: disable=too-many-arguments
  def __init__(
    self,
    grids: int = 10,
    color: str = "white",
    background: str = "whitesmoke",
    subgrids: int = 5,
    scolor: str = "white",
  ):
    self.grids = grids
    self.color = color
    self.background = background
    self.scolor = scolor
    self.subgrids = subgrids

  def draw_background(self, axes: Axes):
    fig = cast(Figure, axes.figure)
    axes.set_facecolor(self.background)
    trans = Affine2D().scale(fig.dpi)
    bbox = axes.get_window_extent().transformed(trans.inverted())
    bbox = cast(Bbox, bbox)
    xy_ratio = bbox.width /bbox.height
    grid_size = 1 / self.grids
    subgrid_size = 1 / (self.grids * self.subgrids)
    i = -grid_size / 2
    while i < 1:
      axes.axvline(i, color=self.scolor, zorder=-1, linewidth=1)
      i += subgrid_size
    i = -grid_size * xy_ratio / 2
    while i < 1:
      axes.axhline(i, color=self.scolor, zorder=-1, linewidth=1)
      i += subgrid_size * xy_ratio
    i = -grid_size/2
    while i < 1:
      axes.axvline(i, color=self.color, zorder=-1, linewidth=3)
      i += grid_size
    i = -grid_size * xy_ratio / 2
    while i < 1:
      axes.axhline(i, color=self.color, zorder=-1, linewidth=3)
      i += grid_size * xy_ratio
