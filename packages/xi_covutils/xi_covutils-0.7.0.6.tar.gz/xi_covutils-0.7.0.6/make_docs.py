#!/usr/bin/env python
"""
Auxiliary Script to update html documentation
"""
from os.path import dirname
from os.path import join
from os import access
from os import makedirs
from os import R_OK
import warnings
import codecs
import pdoc

def html_out(a_module:pdoc.Module):
  """
  Generates HTML output files

  Args:
    a_module (pdoc.Module): A python module.
  """
  file_name = join("docs", a_module.url())
  dirpath = dirname(file_name)
  if not access(dirpath, R_OK):
    makedirs(dirpath)
  with codecs.open(file_name, 'w+', 'utf-8') as writer:
    out = a_module.html(
      external_links=False,
      link_prefix="",
      http_server=False,
    )
    writer.write(out)
  for submodule in a_module.submodules():
    html_out(submodule)

def make_docs():
  """
  Generates documentation
  """
  warnings.filterwarnings(
    action = "ignore",
    category = UserWarning
  )
  print("... Building html files")
  pdoc.tpl_lookup.directories = ["pdoc_templates"] + pdoc.tpl_lookup.directories
  module = pdoc.import_module("xi_covutils")
  module = pdoc.Module(
    module,
  )
  html_out(module)

if __name__ == "__main__":
  print("Creating distribution documentation")
  make_docs()
