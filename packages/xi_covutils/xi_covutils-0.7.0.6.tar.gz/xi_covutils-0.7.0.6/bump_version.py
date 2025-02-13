#!/usr/bin/env python
"""
XI Cov Utils - Bump Version
"""
import os
import sys
from datetime import datetime
from typing import List, Literal, Optional, Tuple, Union

import click

VERSION_FILE = "VERSION"

Rank = Union[
  Literal['major'],
  Literal['minor'],
  Literal['patch'],
  Literal['revision']
]

VersionType = Tuple[int, int, int, Optional[int]]

def current_version() -> Optional[VersionType]:
  """
  Reads the current Version from the VERSION file.

  Returns:
      Optional[VersionType]: The version numbers.
  """
  with open(VERSION_FILE, "r", encoding="utf-8") as f_in:
    version_line = [line.strip() for line in f_in]
    version_line = [l for l in version_line if l]
    if not len(version_line) == 1:
      return None
    try:
      version_tags: List[int] = [
        int(x) for x in version_line[0].split(".")
      ]
    except ValueError:
      return None
    if len(version_tags) < 3 or len(version_tags)>4:
      return None
    revision_tag = None
    if len(version_tags) == 4:
      revision_tag = version_tags[3]
    return (
      version_tags[0],
      version_tags[1],
      version_tags[2],
      revision_tag,
    )

def update_version(c_version: VersionType, rank:str) -> VersionType:
  """
  Updates the given Version at the given rank.

  Args:
      c_version (VersionType): The current given version.
      rank (str): The rank of the Version to be updated:
        ['major', 'minor', 'patch', 'revision'].

  Returns:
      VersionType: The updated Version.
  """
  if rank == "major":
    c_version = (c_version[0] + 1, 0, 0, None)
  if rank == "minor":
    c_version = (c_version[0], c_version[1] + 1, 0, None)
  if rank == "patch":
    c_version = (c_version[0], c_version[1], c_version[2] + 1, None)
  if rank == "revision":
    if not c_version[3]:
      c_version = (c_version[0], c_version[1], c_version[2], 1)
    else:
      c_version = (c_version[0], c_version[1], c_version[2], c_version[3]+1)
  return c_version

def str_version(version: VersionType) -> str:
  """
  Converts the given Version to a str.

  Args:
      version (VersionType): A Version.

  Returns:
      str: A string representing the version.
  """
  ver = [
    str(x)
    for x in version
    if x is not None
  ]
  return ".".join(ver)

def update_pyproject(new_version: str):
  """
  Updates the version in the file 'setup.py'.

  Args:
      new_version (str): A Version.
  """
  with open("pyproject.toml", "r", encoding="utf-8") as f_in:
    lines = f_in.readlines()
  new_lines = []
  for line in lines:
    if line.startswith("version"):
      new_lines.append(f"""version = "{new_version}"\n""")
      continue
    new_lines.append(line)
  with open("pyproject.toml", "w", encoding="utf-8") as f_out:
    f_out.writelines(new_lines)

def update_app_dot_py(new_version: str):
  """
  Updates Version in 'xi_covutils/xi-covutils-app.py' files.

  Args:
      new_version (str): A Version.
  """
  infile = os.path.join(
    "xi_covutils",
    "xi_covutils_app.py"
  )
  with open(infile, "r", encoding="utf-8") as f_in:
    lines = f_in.readlines()
  new_lines = []
  for line in lines:
    if line.startswith("VERSION"):
      new_lines.append(f"""VERSION = "{new_version}"\n""")
      continue
    new_lines.append(line)
  with open(infile, "w", encoding="utf-8") as f_out:
    f_out.writelines(new_lines)

def update_version_file(new_version:str):
  """
  Updates Version in 'VERSION' file.

  Args:
      new_version (str): A Version.
  """
  with open("VERSION", "w", encoding="utf-8") as f_out:
    f_out.write(f"{new_version}")

def get_current_formatted_date() -> str:
  """
  Get the current date as a formatted str.

  Returns:
    str: A Version
  """
  current_day = datetime.now().day
  current_month = datetime.now().month
  current_year = datetime.now().year
  return f"{current_year}-{current_month:02d}-{current_day:02d}"

def update_change_log_file(new_version: str):
  """
  Updates the Version in 'CHANGELOG.md' file.

  Args:
      new_version (str): A Version.
  """
  infile = "CHANGELOG.md"
  with open(infile, "r", encoding="utf-8") as f_in:
    lines = f_in.readlines()
  new_lines = []
  not_found = True
  ntags = len(new_version.split("."))
  date = get_current_formatted_date()
  for line in lines:
    if line.startswith("##") and not_found:
      not_found = False
      if ntags == 4:
        new_lines.append(f"## {new_version} {date}\n")
      if ntags == 3:
        new_lines.append(f"## {new_version} {date}\n\n")
        new_lines.append(line)
      continue
    new_lines.append(line)
  with open(infile, "w", encoding="utf-8") as f_out:
    f_out.writelines(new_lines)

@click.command()
@click.argument(
  "rank",
  type=click.Choice(
    ['major', 'minor', 'patch', 'revision'],
    case_sensitive=False
  ),
  default="revision"
)
def bump_version(rank: Rank):
  """
  Bumps the Version of the package to the next version.

  Args:
    rank (Rank): The rank of the version to bump.
      ['major', 'minor', 'patch', 'revision']
  """
  c_version = current_version()
  if not c_version:
    print("VERSION file has wrong format.")
    sys.exit(1)
  u_version = str_version(update_version(c_version, rank))
  update_pyproject(u_version)
  update_app_dot_py(u_version)
  update_change_log_file(u_version)
  update_version_file(u_version)
  print("Please update CHANGELOG file.")

if __name__ == "__main__":
  bump_version(None) #pylint: disable=no-value-for-parameter
