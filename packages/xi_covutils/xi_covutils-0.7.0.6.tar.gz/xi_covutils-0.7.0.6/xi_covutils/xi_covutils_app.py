#!/usr/bin/env python
"""
XI Cov Utils - Command line interface
"""
import warnings

import click
from Bio import BiopythonDeprecationWarning

from xi_covutils.primers.infer import (
  count_matches, guess, inspect, mismatch_histogram
)

with warnings.catch_warnings():
  warnings.simplefilter(
    action="ignore",
    category=BiopythonDeprecationWarning
  )
  from xi_covutils.conservation import calculate_conservation, conservation_plot
  from xi_covutils.msa import compare_msas

VERSION = "0.7.0.6"

@click.group()
def cli():
  """Main group of CLI commands
  """
  click.echo(f"# XI - Cov Utils {VERSION}")

@click.group()
def msa():
  """
  MSA commands group
  """

msa.add_command(calculate_conservation)
msa.add_command(conservation_plot)
msa.add_command(compare_msas)

@click.group()
def seqs():
  """
  Sequence commands.
  """


cli.add_command(msa)
cli.add_command(seqs)

seqs.add_command(guess)
seqs.add_command(inspect)
seqs.add_command(count_matches)
seqs.add_command(mismatch_histogram)

if __name__ == "__main__":
  cli()
