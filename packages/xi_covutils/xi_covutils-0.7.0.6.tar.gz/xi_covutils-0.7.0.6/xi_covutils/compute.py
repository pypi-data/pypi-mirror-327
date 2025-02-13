"""
Compute covariation using external programs.
"""
from os import close, remove
from shutil import which
from subprocess import CalledProcessError, check_output
from tempfile import mkstemp
from itertools import combinations
from typing import Optional
from Bio.SeqIO import parse
from Bio.Seq import Seq
from Bio.SeqIO import write

from xi_covutils.distances import Distances

ResChain = tuple[str, int]

def cummulative(
  scores:dict[tuple[tuple[str, int], tuple[str, int]], float],
  cutoff:float=6.5
) -> dict[tuple[str, int], float]:
  """
  Compute Cummulative scores.

  Cummulative scores are generalization of cMI scores calculated for MI.

  Return a new dict, which keys has the form (chain_a, index_a),
  and the values are the cummulative covariation scores.

  Args:
    scores (_type_): The covariations scores. A dictionary which keys has the
      form ((chain_a, index_a), (chain_b, index_b)) and the values are the
      covariation scores.
    cutoff (float, optional): The cutoff value to sum a covariation score.
      Defaults to 6.5.

  Returns:
    list: The cumulativ covariation scores.
  """
  cum_cov = {
    k: 0.0
    for pairs in scores
    for k in pairs
  }
  for ((chain_a, index_a), (chain_b, index_b)), value in scores.items():
    if chain_a == chain_b and value >= cutoff:
      cum_cov[(chain_a, index_a)] += value
      cum_cov[(chain_b, index_b)] += value
  return cum_cov

def proximity(
  cum_scores:dict[tuple[str, int], float],
  distances:Distances,
  distance_cutoff:float=6.05
):
  """
  Computes Proximity scores.

  Proximity scores are generalization of pMI scores calculated for MI.

  Args:
    scores(dict[tuple[str, int], float]): a dictionary which keys has the form
      ((chain_a, index_a), (chain_b, index_b)) and the values are the
      covariation scores.
    distances(Distances): a xi_covutils.distances.Distances object.
    distance_cutoff(float): residues within this distances are included for
      proximity scores.

  Returns:
    Return a new dict, which keys has the form (chain_a, index_a),
      and the values are the proximity covariation scores.
  """
  prox_cov = {k: [] for k in cum_scores}
  for (chain_a, index_a), (chain_b, index_b) in combinations(cum_scores, 2):
    c_dist = distances.of(chain_a, index_a, chain_b, index_b)
    if chain_a == chain_b and c_dist and c_dist <= distance_cutoff:
      prox_cov[(chain_a, index_a)].append(cum_scores[(chain_b, index_b)])
      prox_cov[(chain_b, index_b)].append(cum_scores[(chain_a, index_a)])
  prox_cov = {k: float(sum(v))/(max(1, len(v))) for k, v in prox_cov.items()}
  return prox_cov

def export_raw_sequences(
    input_fasta:str,
    output_file:str
  ):
  """
  Exports raw sequences from a fasta file to another file.
    input_fasta(str): path to the input fasta file
    output_file(str): path to the output file.
  """
  records = parse(input_fasta, 'fasta')
  with open(output_file, 'w', encoding='utf-8') as handle:
    for record in records:
      handle.write(str(record.seq)+"\n")

# pylint: disable=too-many-arguments
def ccmpred(
    input_fasta:str,
    outfile:str,
    log_file:Optional[str]=None,
    arguments:Optional[dict[str, str]]=None,
    log_header:str="",
    ccmpred_exec:str='ccmpred'
  ) -> tuple[bool, str]:
  """
  Computes covariation using the external program ccmpred.

  It expects that ccmpred executable to be accesible on the PATH.

  Args:
    input_fasta(str): A fasta formated MSA.
    outfile(str): The path to the output file.
    log_file(Optional[str]): The path to the log file. The log file is open for
      appending. Defaults to None.
    arguments(Optional[dict[str, str]]): Additional arguments to pass to
      ccmpred. Defaults to None.
    log_header(str): An identifier for the current run on the log file.
    ccmpred(str): The name of the the executable program.

  Returns:
    tuple[bool, str]: A tuple where the first element is a succes value and the
      second is an error message if calculations was not succesful.
  """
  success = (False, "")
  if not (tmp := which(ccmpred_exec)):
    return (False, "CCMpred program was not found in the path")
  ccmpred_exec = tmp
  raw_seq_handle, raw_seq_file_path = mkstemp(suffix="raw", text=True)
  close(raw_seq_handle)
  try:
    export_raw_sequences(input_fasta, raw_seq_file_path)
  except FileNotFoundError as err:
    return (False, str(err))
  if not arguments:
    ccmpred_arguments:dict[str, str] = {}
  else:
    ccmpred_arguments:dict[str, str] = arguments
  cmd = (
    [ccmpred_exec] +
    [str(k) for arg in ccmpred_arguments.items() for k in arg] +
    [raw_seq_file_path, outfile]
  )
  success = run_and_log(
    cmd,
    input_fasta,
    log_file,
    log_header
  )
  remove(raw_seq_file_path)
  return success

class Logger():
  """
  A context manager for logging.
  """
  def __init__(self, logfile:Optional[str]=None):
    self.file = logfile
    self.log_handle = None
  def __enter__(self):
    if self.file:
      self.log_handle = open(self.file, 'a', encoding='utf-8')
    return self
  def __exit__(self, c_type, value, traceback):
    if self.log_handle:
      self.log_handle.close()
    return self
  def write(self, data):
    """
    Write data in opened log handle.
    Args:
      data: data to write into the log file.
    """
    if self.log_handle:
      self.log_handle.write(data)


def run_and_log(
    command:list[str],
    input_fasta:str,
    log_file:Optional[str],
    log_header:str=""
  ) -> tuple[bool, str]:
  """
  Run covariation and logs the output.

  Args:
    command(list[str]): a command line as a list of strings.
    input_fasta(str): the path to the input MSA in fasta format.
    log_file(Optional[str]): The path to the log file.
    log_header(str): An identifier for the current run on the log file.
  """
  with Logger(log_file) as log_handle:
    try:
      log_handle.write(f"Computing cov for [{log_header}]\n")
      out_text = check_output(command)
      out_text = out_text.decode()
      log_handle.write(out_text)
      success = (True, str(out_text))
    except CalledProcessError as err:
      log_handle.write(f"Error on: {input_fasta} {command}")
      log_handle.write(f"Error Code: {err.returncode}")
      log_handle.write(f"Error Message:\n{err.output}")
      success = (False, str(err))
  return success

def mutual_info(
    input_fasta:str,
    outfile:str,
    log_file:Optional[str]=None,
    arguments:Optional[dict[str, str]]=None,
    log_header:str="",
    julia_script:str='Buslje09.jl'
  ) -> tuple[bool, str]:
  """
  Computes covariation using the external MIToS script Buslje09.jl for julia
  language.

  It expects that 'Buslje09.jl' executable to be accesible on the PATH, and that
  it will be interpreted by the correct version of julia.
  Hint: Check the shebang comment in the script file.

  Args:
    input_fasta(str): A fasta formated MSA.
    outfile(str): The path to the output file.
    log_file(Optional[str]): The path to the log file. The log file is open for
      appending.
    arguments(Optinal[dict[str, str]]): Additional arguments to pass to ccmpred.
      Defaults to None.
    log_header(str): An identifier for the current run on the log file.
    julia_script(str): The name of the the executable program. Defaults to
      "Buslje09.jl".

  Returns:
    tuple[bool, str]: A tuple where the first element is a succes value and the
      second is an error message if calculations was not succesful.
  """
  success = (False, "")
  julia_exec = which(julia_script)
  if not julia_exec:
    raise ValueError("Buslje09.jl script could not be found in path")
  base_arguments = {"--format": "FASTA", "--output": outfile}
  arguments = {} if not arguments else arguments
  base_arguments.update(arguments)
  cmd = (
    [julia_exec] +
    [str(k) for arg in base_arguments.items() for k in arg] +
    [input_fasta]
  )
  success = run_and_log(cmd, input_fasta, log_file, log_header)
  return success

def fix_msa_for_gauss(input_fasta:str) -> str:
  """
  Fixes the input MSA to the requirements of gaussDCA.

  Characters are converted to uppercase, and '.' are converted to '-'
  Returns a path to the converted temporary file.
  The user of the function is responsible to remove the file after use.
  Args:
    input_fasta(str): path of the input fasta file.
  Returns:
    str: The file path of the output file.
  """
  records = list(parse(input_fasta, format="fasta"))
  for record in records:
    record.seq = Seq(str(record.seq.upper()).replace(".", "-"))
  file_open, temp_file = mkstemp(suffix=".fasta")
  close(file_open)
  with open(temp_file, 'w', encoding='utf-8') as temp_file_handle:
    write(records, temp_file_handle, format='fasta')
  return temp_file

#pylint: disable=too-many-locals
def gauss_dca(
    input_fasta:str,
    outfile:str,
    log_file:Optional[str]=None,
    arguments:Optional[dict[str, str]]=None,
    log_header:str="",
    julia:str='julia'
  ) -> tuple[bool, str]:
  """
  Computes covariation using the a external julia script.

  It expects that 'julia' executable to be accesible on the PATH, and that
  has installed gaussDCA package.

  Args:
    input_fasta(str): A fasta formated MSA.
    outfile(str): The path to the output file.
    log_file(Optional[str]): The path to the log file. The log file is open for
      appending.
    arguments(Optional[dict[str, str]]): Additional arguments to pass to
      ccmpred. Defaults to None.
    log_header(str): An identifier for the current run on the log file.
    julia(str): The name of the the executable program. Defaults to
      "Buslje09.jl"

  Returns:
    tuple[bool, str]: A tuple where the first element is a succes value and the
      second is an error message if calculations was not succesful.
  """
  def _prepare_arguments(fixed_input_fasta, arguments):
    base_arguments = {"min_separation": "1"}
    arguments = {} if not arguments else arguments
    base_arguments.update(arguments)
    first_argument = f'"{fixed_input_fasta}"'
    additional_arguments = ", ".join(
      f"{k}={v}" for k, v in base_arguments.items()
    )
    if additional_arguments:
      base_arguments = f"{first_argument}, {additional_arguments}"
    else:
      base_arguments = first_argument
    return base_arguments

  success = (False, "")
  julia_exec = which(julia)
  if not julia_exec:
    raise ValueError("julia script could not be found in path")
  raw_seq_handle, raw_seq_file_path = mkstemp(suffix="raw", text=True)
  close(raw_seq_handle)
  fixed_input_fasta = fix_msa_for_gauss(input_fasta)
  base_arguments = _prepare_arguments(fixed_input_fasta, arguments)
  temp_script_handle, temp_script = mkstemp(suffix='.jl')
  close(temp_script_handle)
  with open(temp_script, 'w', encoding='utf8') as script_handle:
    script_handle.write(
      f'using GaussDCA; printrank("{outfile}", gDCA({base_arguments}))'
    )
  success = run_and_log(
    [julia_exec, temp_script],
    input_fasta,
    log_file,
    log_header
  )
  remove(raw_seq_file_path)
  remove(fixed_input_fasta)
  remove(temp_script)
  return success
