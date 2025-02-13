#!usr/bin/env python3
"""
  Run radon complexity analyzer
"""
import sys
from os import listdir
from os.path import join
from functools import reduce
import argparse
from radon.complexity import cc_rank, cc_visit

def run_radon():
  """
    Runs radon
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-a',
    '--all',
    help="echo show all code elements in output",
    action="store_true"
  )
  args = parser.parse_args()
  show_all = args.all
  module_folder = "xi_covutils"
  source_files = (
    join(module_folder, fn)
    for fn in listdir(module_folder)
    if fn.endswith(".py")
  )
  all_results, filtered_results, n_high = filter_high_complexity(source_files)

  _make_output(all_results if show_all else filtered_results)
  sys.exit(1 if n_high > 0 else 0)

def _make_output(results):
  for source_file, cc_result in results:
    for element_result in cc_result:
      print(
        f"{source_file:30s} | "
        f"{cc_rank(element_result.complexity)} | "
        f"{str(element_result):40s}"
      )

def filter_high_complexity(source_files):
  """
  Filter source elements that has high complexity
    :param source_files: a list of str with the path of the source files
  """
  def filter_hc(results):
    return [e for e in results if cc_rank(e.complexity) > 'C']
  all_results = []
  for src_file in source_files:
    with open(src_file, "r", encoding="utf-8") as f_in:
      all_results.append((src_file, cc_visit(f_in.read())))
  filtered_results = [
    (sf, filter_hc(cc_result))
    for sf, cc_result in all_results
  ]
  n_high = reduce(lambda a, b: a+b, [len(x) for _, x in filtered_results])
  return all_results, filtered_results, n_high

if __name__ == "__main__":
  run_radon()
