"""
BlastP classes and functions
"""
from io import StringIO
import subprocess
from typing import Any, Literal, Optional, Union

import pandas as pd

Blastptask = Union[
  Literal["blastp"],
  Literal["blastp-fast"],
  Literal["blastp-short"]
]

Blastntask = Union[
  Literal["blastn"],
  Literal["blastn-short"],
  Literal["dc-megablast"],
  Literal["megablast"],
  Literal["rmblastn"]
]

class BlastResult:
  """
  BlastResult. Represent the results of a blast search.
  """

  def __init__(self):
    self.data:list[list[Any]] = []
    self.headers:list[str] = []

  def __len__(self) -> int:
    """
    Returns the number of data rows in the BlastResult object.
    """
    return len(self.data)

  def set_headers(self, headers:list[str]):
    """
    Sets the headers for the data fields in the BlastResult object.
    Args:
      headers (list[str]): The headers for the data fields.
    """
    self.headers = headers

  def has_headers(self) -> bool:
    """
    Checks if the BlastResult object has headers.

    Returns:
      bool: True if headers are set, False otherwise.
    """
    return bool(self.headers)

  def add(self, row:list[Any]):
    """
    Adds a row of data to the BlastResult object.

    Args:
      row (list[Any]): A row of data.
    """
    if not len(row) == len(self.headers):
      raise ValueError(
        f"Data has {len(row)} fields, header has {len(self.headers)} fields"
      )
    self.data.append(row)

  def exclude(self, header:str, values:set[Any]) -> "BlastResult":
    """
    Removes those hits from the BlastResult that matches with any of the
    given values in the given header.

    Args:
      header (str): A header name.
      values (set[Any]): A set of values to exclude.

    Returns:
      BlastResult: The modified BlastResult object.
    """
    try:
      col_index = self.headers.index(header)
    except ValueError:
      return self
    self.data = [
      row
      for row in self.data
      if not row[col_index] in values
    ]
    return self


  def as_dataframe(self) -> pd.DataFrame:
    """
    Convert the results as a pandas DataFrame.

    Returns:
      pd.DataFrame: A pandas Dataframe.
    """
    dataframe = pd.DataFrame(
      self.data,
      columns = self.headers
    )
    return dataframe

  @staticmethod
  def _parse_fields(line:str) -> list[Union[str, int, float]]:
    """
    Parses a line of data and returns a list of fields.

    Args:
      line (str): A line of data.

    Returns:
      list[Union[str, int, float]]: A list of fields parsed from the line of
        data.
    """
    fields = []
    for c_field in line.split("\t"):
      try:
        c_field = int(c_field)
        fields.append(c_field)
        continue
      except ValueError:
        pass
      try:
        c_field = float(c_field)
        fields.append(c_field)
        continue
      except ValueError:
        pass
      fields.append(c_field)
    return fields

  @staticmethod
  def from_tabular_with_headers(input_data) -> "BlastResult":
    """
    Creates a BlastResult object from tabular data with headers.

    Args:
      input_data: The tabular data with headers.

    Returns:
      BlastResult: A BlastResult object.
    """
    result = BlastResult()
    for line in input_data:
      line = line.rstrip()
      if line.startswith("# Fields: "):
        if not result.has_headers():
          line = line[10:]
          fields = [x.strip() for x in line.split(",")]
          result.set_headers(fields)
        continue
      if line.startswith("#"):
        continue
      fields = BlastResult._parse_fields(line)
      result.add(fields)
    return result

  @staticmethod
  def from_tabular_without_headers(
      headers: list[str],
      input_data
    ) -> "BlastResult":
    """
    Creates a BlastResult object from tabular data without headers.

    Args:
      headers (list[str]): The headers for the data fields.
      input_data: The tabular data without headers.

    Returns:
      BlastResult: A BlastResult object.
    """
    result = BlastResult()
    result.set_headers(headers)
    for line in input_data:
      line = line.rstrip()
      fields = BlastResult._parse_fields(line)
      result.add(fields)
    return result

class BlastWrapper: # pylint: disable=too-many-instance-attributes
  """
  A abstract wrapper for blast commands.
  Do not use this class. Use BlastP or BlastN classes.
  """

  def __init__(self):
    self.command: str = ""
    self.query: Optional[str] = None
    self.query_string: Optional[str] = None
    self.database: Optional[str] = None
    self.subject: Optional[str] = None
    self.args: list[str] = []
    self.fields = ["std"]
    self.evalue: float = 1E-5
    self.outfile: Optional[str] = None
    self.task: str = ""

  def with_executable_command(self, blast_command:str) -> "BlastWrapper":
    """
    Sets the path of the current blast executable.

    Args:
      blast_command (str): Path to the blast command.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.command = blast_command
    return self

  def with_query_string(self, query:str) -> "BlastWrapper":
    """
    Set the query sequence as a string.

    Args:
      query (str): The input sequence.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.query_string = query
    return self

  def with_query(self, query_file:str) -> "BlastWrapper":
    """
    Sets the query file.

    Args:
      query_file (str): The path of the query file.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.query = query_file
    return self

  def with_db(self, db_path:str) -> "BlastWrapper":
    """
    Set the Database to search.
    Incomptible with subject.

    Args:
      db_path (str): The path prefix to the database.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.database = db_path
    self.subject = None
    return self

  def with_subject(self, subject_path:str) -> "BlastWrapper":
    """
    Set the subject file for the search.
    Incompatible with db.

    Args:
      subject_path (str): Path to a file with the subjects.

    Returns:
      'BlastWrapper': A BlastWrapper wrapper class.
    """
    self.subject = subject_path
    self.query = None
    return self

  def with_evalue(self, evalue:float) -> "BlastWrapper":
    """
    Sets the e-value.

    Args:
      evalue (float): The e-value threshold for saving hits.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.evalue = evalue
    return self

  def with_arguments(self, *args:Any) -> "BlastWrapper":
    """
    Adds additional arguments to the BlastWrapper command.

    Args:
      *args (Any): Additional arguments for the BlastWrapper command.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    str_args = [str(x) for x in args]
    self.args.extend(str_args)
    return self

  def with_output_file(self, outfile:str) -> "BlastWrapper":
    """
    Sets the output file for the BlastWrapper results.

    Args:
      outfile (str): Path to the output file.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.outfile = outfile
    return self

  def with_output_fields(self, fields:list[str]) -> "BlastWrapper":
    """
    Sets the output fields for the BlastWrapper results.

    Args:
      fields (list[str]): List of fields to include in the output.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.fields = fields
    return self

  def with_output_fields_std(self) -> "BlastWrapper":
    """
    Sets the output fields to the standard fields.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.fields = ["std"]
    return self

  def with_output_fields_std_plus(self, fields:list[str]) -> "BlastWrapper":
    """
    Sets the output fields to the standard fields plus additional specified
      fields.

    Args:
      fields (list[str]): Additional fields to include in the output.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.fields = ["std"] + fields
    return self

  def with_output_fields_recommended(self) -> "BlastWrapper":
    """
    Sets the output fields to the standard fields plus qcovs and staxid.

    Returns:
      'BlastWrapper': A BlastWrapper command wrapper class.
    """
    self.fields = ["std", "qcovs", "staxid"]
    return self

  def _run_with_query_string(self) -> subprocess.CompletedProcess:
    """
    Executes the blast command with the query sequence provided as a string.

    Returns:
      CompletedProcess: An object that represents the completed execution of
        the blast command.
    """
    cmd = self.running_command()
    proc = subprocess.run(
      cmd,
      check=False,
      capture_output=True,
      input=self.query_string,
      text=True,
    )
    return proc

  def _run_with_input_file(self):
    """
    Executes the blast command with the query sequence provided as an input
      file.

    Returns:
      CompletedProcess: An object that represents the completed execution of
        the blast command.
    """
    cmd = self.running_command()
    proc = subprocess.run(
      cmd,
      check=False,
      capture_output=True,
      text=True,
    )
    return proc

  def run(self) -> tuple[Optional[BlastResult], str]:
    """
    Runs the blast command and returns the result and any errors.

    Returns:
      tuple[Optional[BlastResult], str]: A tuple containing the BlastResult
        object (or None if results are save to a file) and any error messages.
    """
    if self.query_string:
      proc = self._run_with_query_string()
    else:
      proc = self._run_with_input_file()
    error = proc.stderr
    if self.outfile:
      return None, error
    bresult = BlastResult.from_tabular_with_headers(
      StringIO(proc.stdout)
    )
    return bresult, error

  def running_command_string(self) -> str:
    """
    Generates the full string of the blast command that will be executed.

    Returns:
      str: A string of the blast command that will be executed.
    """
    return " ".join(self.running_command())

  def running_command(self) -> list[str]:
    """
    Generates the command list for the blast process.

    Returns:
      list[str]: A list containing the blast command and its arguments that
        will be executed.

    Raises:
      ValueError: If neither a database nor a subject, or both, are provided.
      ValueError: If neither a query file nor a query string, or both, are
        provided.
    """
    if (
      (not self.database and not self.subject) or
      (self.database and self.subject)
    ):
      raise ValueError("Blast Wrapper needs a db value or a subject.")
    if (
      (not self.query and not self.query_string) or
      (self.query and self.query_string)
    ):
      raise ValueError("Blast Wrapper needs a query or a query_string")
    cmd = [
      self.command,
      '-query',
      self.query if self.query else "-",
    ]
    if self.database:
      cmd.append('-db')
      cmd.append(self.database)
    if self.subject:
      cmd.append('-subject')
      cmd.append(self.subject)
    cmd.append("-outfmt")
    cmd.append(f"7 {' '.join(self.fields)}")
    if self.outfile:
      cmd.append("out")
      cmd.append(self.outfile)
    cmd.extend(self.args)
    cmd.append("-task")
    cmd.append(self.task)
    cmd.append("-evalue")
    cmd.append(str(self.evalue))
    return cmd

class BlastP(BlastWrapper): # pylint: disable=too-many-instance-attributes
  """
  Wrapper for local blastp command.

  Creates a the command line to perform a blast search and
  can execute the command.

  No makes an extensive check of all blastp arguments before running.
  """
  def __init__(self):
    super().__init__()
    self.command: str = "blastp"
    self.task: Blastptask = "blastp"

  def with_task(self, task: Blastptask) -> "BlastP":
    """
    Sets the BLASTP task type.

    Args:
      task (Blastptask): The BLASTP task to perform.

    Returns:
      'BlastP': A BlastP command wrapper class.
    """
    self.task = task
    return self

class BlastN(BlastWrapper): # pylint: disable=too-many-instance-attributes
  """
  Wrapper for local blastn command.

  Creates a the command line to perform a blast search and
  can execute the command.

  No makes an extensive check of all blastn arguments before running.
  """
  def __init__(self):
    super().__init__()
    self.command: str = "blastn"
    self.task: Blastntask = "blastn"

  def with_task(self, task: Blastntask) -> "BlastN":
    """
    Sets the BLASTN task type.

    Args:
      task (Blastntask): The BLASTN task to perform.

    Returns:
      'BlastN': A BlastN command wrapper class.
    """
    self.task = task
    return self
