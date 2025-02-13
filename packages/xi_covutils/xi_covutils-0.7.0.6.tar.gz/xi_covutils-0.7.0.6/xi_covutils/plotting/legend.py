"""
Helper functions for creating custom legends.
"""
from matplotlib import patches
from matplotlib.legend_handler import HandlerBase

class ManyRectangleHandler(HandlerBase):
  """
  A legend handler that creates a rectangle for each color in the list.
  """
  def __init__(self, colors:list[str], **kwargs):
    self.colors = colors
    super().__init__(**kwargs)
  # pylint: disable=too-many-arguments
  def create_artists(
    self, legend, orig_handle,
    xdescent, ydescent,
    width, height,
    fontsize, trans
  ):
    spacer = width/10
    n_boxes = len(self.colors)
    box_width = (width - (n_boxes-1)*spacer)/n_boxes
    artists = [
      patches.Rectangle(
        (xdescent + i*(box_width + spacer), ydescent),
        box_width, height,
        facecolor=color, transform=trans
      )
      for i, color in enumerate(self.colors)
    ]
    return artists
