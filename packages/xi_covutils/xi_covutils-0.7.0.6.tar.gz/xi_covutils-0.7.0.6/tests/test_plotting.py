"""Tests for plotting module."""
import os
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pandas as pd
import numpy as np
from pytest import approx
import pytest
from xi_covutils.plotting.background import (
  LightColorSquaredBackground,
  RandomLightColorSquaredBackground,
  GridBackground,
  SubGridsBackground
)
from xi_covutils.plotting.boxplot import (
    PlainColorBoxplotPrecomputedTheme,
    precompute_boxplot_data
)
from xi_covutils.plotting.grouper import (
  ElementGrouperWithSpacers,
  ElementGrouperSimple
)

#pylint: disable=missing-class-docstring
#pylint: disable=missing-function-docstring
#pylint: disable=too-few-public-methods

class TestTicksGrouperWithSpacers:
  def test_get_positions(self):
    groups = [3, 2, 1]
    grouper = ElementGrouperWithSpacers(groups, 0.2, 0.5)
    expected = approx([0, 0.2, 0.4, 0.9, 1.1, 1.6])
    assert grouper.get_element_positions() == expected

  def test_get_xticks(self):
    groups = [3, 2, 1]
    grouper = ElementGrouperWithSpacers(groups, 0.2, 0.5)
    assert grouper.get_group_positions() == approx([0.2, 1.0, 1.6])

class TestTicksGrouperSimple:
  def test_get_positions(self):
    groups = [3, 2, 1]
    grouper = ElementGrouperSimple(groups, 0.2)
    expected = approx([0.2, 1.0, 1.8, 3.1, 3.9, 5])
    assert grouper.get_element_positions() == expected
    groups = [3, 2, 1, 4]
    grouper = ElementGrouperSimple(groups, 0.3)
    expected = approx(
      [0.3, 1.0, 1.7, 3.15, 3.85, 5, 6.45, 7.15, 7.85, 8.55]
    )
    assert grouper.get_element_positions() == expected
  def test_get_xticks(self):
    groups = [3, 2, 1]
    grouper = ElementGrouperSimple(groups, 0.2)
    assert grouper.get_group_positions() == approx([1.0, 3.5, 5])
    groups = [3, 2, 1, 4]
    grouper = ElementGrouperSimple(groups, 0.3)
    assert grouper.get_group_positions() == approx(
      [1.0, 3.5, 5.0, 7.50]
    )


def _get_image_array(canvas: FigureCanvasAgg):
  buffer = canvas.tostring_argb()
  width, height = canvas.get_width_height()
  image_array = (
    np.frombuffer(buffer, dtype=np.uint8)
      .reshape(height * width, 4)
  )
  data = (
    pd.DataFrame(
      image_array,
      columns=["alpha", "red", "green", "blue"]
    )
    .assign(
      row = lambda x: x.index // width,
      col = lambda x: x.index % width,
    )
    .set_index(["row", "col"], drop=True)
  )
  return data


def _load_imagearray_from_file(filename):
  data = (
    pd.read_csv(filename, sep="\t")
      .set_index(["row", "col"])
  )
  return data


class TestLightColorSquaredBackground:
  def test_draw_background(self, test_data_folder):
    fig, axes = plt.subplots(figsize=(1, 1))
    background = LightColorSquaredBackground()
    background.draw_background(axes)
    canvas = fig.canvas
    if not isinstance(canvas, FigureCanvasAgg):
      pytest.skip("This test requires the Agg backend")
    canvas.draw()
    image_array = _get_image_array(canvas)
    expected = _load_imagearray_from_file(
      os.path.join(test_data_folder, "image_array_01.csv")
    )
    assert image_array.to_numpy() == approx(expected.to_numpy(), abs=5)


class TestRandomLightColorSquaredBackground:
  def test_draw_background(self, test_data_folder):
    fig, axes = plt.subplots(figsize=(1, 1))
    background = RandomLightColorSquaredBackground(
      n_boxes=3,
      intensity=0.5,
      randomness=0.5,
      color="black"
    )
    background.draw_background(axes)
    canvas = fig.canvas
    if not isinstance(canvas, FigureCanvasAgg):
      pytest.skip("This test requires the Agg backend")
    canvas.draw()
    image_array = _get_image_array(canvas)
    expected = _load_imagearray_from_file(
      os.path.join(test_data_folder, "image_array_02.csv")
    )
    assert image_array.to_numpy() == approx(expected.to_numpy(), abs=5)


class TestGridBackground:
  def test_draw_background(self, test_data_folder):
    fig, axes = plt.subplots(figsize=(1.5, 0.75))
    background = GridBackground(
      grids=4,
      color="black"
    )
    background.draw_background(axes)
    canvas = fig.canvas
    if not isinstance(canvas, FigureCanvasAgg):
      pytest.skip("This test requires the Agg backend")
    canvas.draw()
    image_array = _get_image_array(canvas)
    expected = _load_imagearray_from_file(
      os.path.join(test_data_folder, "image_array_03.csv")
    )
    assert image_array.to_numpy() == approx(expected.to_numpy(), abs=5)


class TestSubGridBackground:
  def test_draw_background(self, test_data_folder):
    fig, axes = plt.subplots(figsize=(1, 1))
    background = SubGridsBackground(
      grids=4
    )
    background.draw_background(axes)
    canvas = fig.canvas
    if not isinstance(canvas, FigureCanvasAgg):
      pytest.skip("This test requires the Agg backend")
    canvas.draw()
    image_array = _get_image_array(canvas)
    expected = _load_imagearray_from_file(
      os.path.join(test_data_folder, "image_array_04.csv")
    )
    assert image_array.to_numpy() == approx(expected.to_numpy(), abs=5)


class TestPlainColorBoxplotPrecomputedTheme:
  def test_do_no_fail(self):
    original_backend = plt.get_backend()
    plt.switch_backend("Agg")
    fig, axis = plt.subplots(1, 1, figsize=(5, 5))
    theme = PlainColorBoxplotPrecomputedTheme(
      axis = axis,
      figure = fig,
      colors = ["red", "green"],
      groups = [1, 1],
      data = [
        {
          "whislo": 1,
          "q1": 3,
          "med": 4,
          "q3": 5,
          "whishi": 7,
          "fliers": []
        },
        {
          "whislo": 1,
          "q1": 3,
          "med": 4,
          "q3": 5,
          "whishi": 7,
          "fliers": []
        },
      ]
    )
    with theme:
      axis.set_title("")
    assert all(
      x in theme.computed_elements
      for x in ['whiskers', 'caps', 'boxes', 'medians', 'fliers', 'means']
    )
    plt.switch_backend(original_backend)

def test_precompute_boxplot_data():
  data = np.array([1, 9, 2, 8, 3, 7, 4, 6, 5])
  precomputed_data = precompute_boxplot_data(data)
  assert precomputed_data == {
    "whislo": 1,
    "q1": 3,
    "med": 5,
    "q3": 7,
    "whishi": 9,
    "fliers": []
  }

def test_precompute_boxplot_data_with_flyers():
  data = np.array([-4, 19, 2, 8, 3, 7, 4, 6, 5])
  precomputed_data = precompute_boxplot_data(data, include_fliers=True)
  assert precomputed_data == {
    "whislo": 2,
    "q1": 3,
    "med": 5,
    "q3": 7,
    "whishi": 8,
    "fliers": [-4, 19]
  }
