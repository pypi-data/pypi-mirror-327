"""
Test configuration
"""
from typing import Iterable
import inspect
from os.path import dirname
from os.path import join
from pytest import fixture, mark, Config, Function, Parser

@fixture(scope="session")
def test_data_folder():
  """
  Test fixture that provides access to a folder with the data required to run
  the tests correctly.
  """
  return join(dirname(inspect.stack()[0][1]), "test_data")

def pytest_addoption(parser: Parser):
  """
  Add option to run tests that requires connection to other services.

  Args:
    parser (Parser): A parser to which add an option.
  """
  parser.addoption(
    "--requires-connection",
    action="store_true",
    default=False,
    help="Runs tests that requires a coonection 3rd party web server."
  )


def pytest_configure(config:Config):
  """
  Modify pytest configuration.

  Args:
    config (Config): A pytest configuration object.
  """
  config.addinivalue_line(
    "markers",
    "requires_connection: mark test as require connection"
  )


def pytest_collection_modifyitems(config: Config, items: Iterable[Function]):
  """
  Modify pytest items collected from source code.

  Args:
    config (Config): A pytest configuraion.
    items (Iterable[Function]): A collection of pytest Functions decorators.
  """
  if config.getoption("--requires-connection"):
    return
  skip_slow = mark.skip(reason="need --requires-connection option to run")
  for item in items:
    if "requires_connection" in item.keywords:
      item.add_marker(skip_slow)
