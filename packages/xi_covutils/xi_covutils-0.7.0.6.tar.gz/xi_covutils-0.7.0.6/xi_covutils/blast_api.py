"""
Makes Blast API calls

From Blast Api documentation

| variable       | value                                                      |
| --------       | -----------------                                          |
| Parameter      | QUERY                                                      |
| Definition     | Search query                                               |
| Type           | String                                                     |
| CMD            | Put *                                                      |
| Allowed values | "Accession, GI, or FASTA."                                 |
| Parameter      | DATABASE                                                   |
| Definition     | BLAST database                                             |
| Type           | String                                                     |
| CMD            | Put *                                                      |
| Allowed values | Database from appendix 2 or one uploaded to blastdb_custom |
|                | (see appendix 4)                                           |
| Parameter      | PROGRAM                                                    |
| Definition     | BLAST program                                              |
| Type           | String                                                     |
| CMD            | Put *                                                      |
| Allowed values | One of blastn, blastp, blastx, tblastn, tblastx. To        |
|                | enable megablast, use PROGRAM=blastn&MEGABLAST=on.         |
| Parameter      | FILTER                                                     |
| Definition     | Low complexity filtering                                   |
| Type           | String                                                     |
| CMD            | Put                                                        |
| Allowed values | F to disable. T or L to enable. Prepend “m” for mask at    |
|                | lookup (e.g., mL)                                          |
| Parameter      | FORMAT_TYPE                                                |
| Definition     | Report type                                                |
| Type           | String                                                     |
| CMD            | "Put, Get"                                                 |
| Allowed values | HTML, Text, XML, XML2, JSON2, or Tabular. HTML is the      |
|                | default.                                                   |
| Parameter      | EXPECT                                                     |
| Definition     | Expect value                                               |
| Type           | Double                                                     |
| CMD            | Put                                                        |
| Allowed values | Number greater than zero.                                  |
| Parameter      | NUCL_REWARD                                                |
| Definition     | Reward for matching bases (BLASTN and megaBLAST)           |
| Type           | Integer                                                    |
| CMD            | Put                                                        |
| Allowed values | Integer greater than zero.                                 |
| Parameter      | NUCL_PENALTY                                               |
| Definition     | Cost for mismatched bases (BLASTN and megaBLAST)           |
| Type           | Integer                                                    |
| CMD            | Put                                                        |
| Allowed values | Integer less than zero.                                    |
| Parameter      | GAPCOSTS                                                   |
| Definition     | Gap existence and extension costs                          |
| Type           | String                                                     |
| CMD            | Put                                                        |
| Allowed values | Pair of positive integers separated by a space such as     |
|                | “11 | 1”.                                                  |
| Parameter      | MATRIX                                                     |
| Definition     | Scoring matrix name                                        |
| Type           | String                                                     |
| CMD            | Put                                                        |
| Allowed values | One of BLOSUM45, BLOSUM50, BLOSUM62, BLOSUM80,BLOSUM90,    |
|                | PAM250, PAM30 or PAM70. Default: BLOSUM62 for all          |
|                | applicable programs                                        |
| Parameter      | HITLIST_SIZE                                               |
| Definition     | Number of databases sequences to keep                      |
| Type           | Integer                                                    |
| CMD            | "Put,Get"                                                  |
| Allowed values | Integer greater than zero.                                 |
| Parameter      | DESCRIPTIONS                                               |
| Definition     | Number of descriptions to print (applies to HTML and Text) |
| Type           | Integer                                                    |
| CMD            | "Put,Get"                                                  |
| Allowed values | Integer greater than zero.                                 |
| Parameter      | ALIGNMENTS                                                 |
| Definition     | Number of alignments to print (applies to HTML and Text)   |
| Type           | Integer                                                    |
| CMD            | "Put,Get"                                                  |
| Allowed values | Integer greater than zero.                                 |
| Parameter      | NCBI_GI                                                    |
| Definition     | Show NCBI GIs in report                                    |
| Type           | String                                                     |
| CMD            | "Put, Get"                                                 |
| Allowed values | T or F                                                     |
| Parameter      | RID                                                        |
| Definition     | BLAST search request identifier                            |
| Type           | String                                                     |
| CMD            | "Get *, Delete *"                                          |
| Allowed values | The Request ID (RID) returned when the search was          |
|                | submitted                                                  |
| Parameter      | THRESHOLD                                                  |
| Definition     | Neighboring score for initial words                        |
| Type           | Integer                                                    |
| CMD            | Put                                                        |
| Allowed values | Positive integer (BLASTP default is 11). Does not apply to |
|                | BLASTN or MegaBLAST.                                       |
| Parameter      | WORD_SIZE                                                  |
| Definition     | Size of word for initial matches                           |
| Type           | Integer                                                    |
| CMD            | Put                                                        |
| Allowed values | Positive integer.                                          |
| Parameter      | COMPOSITION_BASED_STATISTICS                               |
| Definition     | Composition based statistics algorithm to use              |
| Type           | Integer                                                    |
| CMD            | Put                                                        |
| Allowed values | One of 0, 1, 2, or 3. See comp_based_stats command line    |
|                | option in the BLAST+ user manual for details.              |
| Parameter      | FORMAT_OBJECT                                              |
| Definition     | Object type                                                |
| Type           | String                                                     |
| CMD            | Get                                                        |
| Allowed values | SearchInfo (status check) or Alignment (report formatting) |
| Parameter      | NUM_THREADS                                                |
| Definition     | Number of virtual CPUs to use                              |
| Type           | Integer                                                    |
| CMD            | Put                                                        |
| Allowed values | Integer greater than zero and less than the maximum number |
|                | of cores on the instance (default is the maximum number of |
|                | cores on the instance). Supported only on the cloud.       |
"""
from dataclasses import dataclass
import json
import time
from enum import Enum
import re
from typing import Optional, Dict
import requests
from requests.models import Response

qblastinfo_pattern:re.Pattern = re.compile(
  r".*(QBlastInfoBegin.*QBlastInfoEnd).*",
  re.IGNORECASE|re.MULTILINE|re.DOTALL
)
def get_qblast_info(resp: Response) -> Optional[dict[str, str]]:
  """
  Gets the content of a QBlastInfo Block in a http response.

  Args:
    resp (Response): A Response instance after callling NCBI web server.

  Returns:
    Optional[dict[str, str]]: A dictionary with the content of the QBlastInfo
      Block.
  """
  match = re.match(
    qblastinfo_pattern,
    resp.text
  )
  if match:
    lines = match.group(1).split("\n")
    lines = [line.split("=") for line in lines]
    lines = [x for x in lines if len(x)==2]
    result = {
      x[0].strip(): x[1].strip()
      for x in lines
    }
    return result
  return None

class NcbiProgram(Enum):
  """
  The available NCBI programs.
  """
  BLASTN = "blastn"
  BLASTP = "blastp"
  BLASTX = "blastx"
  TBLASTN = "tblastn"
  TBLASTX = "tblastx"

class NcbiDatabase(Enum):
  """
  Available NCBI databases.
  """
  NT = "nt"
  NR = "nr"
  REFSEQ_RNA = "refseq_rna"
  REFSEQ_PROTEIN = "refseq_protein"
  SWISSPROT = "swissprot"
  PDBAA = "pdbaa"
  PDBNT = "pdbnt"

class NcbiBlast:
  """
  The NCBI Blast Class to call the API.
  """
  url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
  def __init__(self) -> None:
    self.megablast:bool = False
    self.program:NcbiProgram = NcbiProgram.BLASTN
    self.database:Optional[NcbiDatabase] = None
    self.rid: Optional[str] = None
    self.built: bool = False
    self.last_response_time: Optional[float] = None
    self.output_buffer: Optional[bytes] = None

  def set_program(self, program: NcbiProgram) -> 'NcbiBlast':
    """
    Sets ths NCBI program.

    Args:
      program (NcbiProgram): A program name.

    Returns:
      'NcbiBlast': Returns self, part of the builder pattern.
    """
    self.program = program
    return self

  def set_megablast(self) -> 'NcbiBlast':
    """
    Sets megablast option.

    Returns:
      'NcbiBlast': Returns self, part of the builder pattern.
    """
    self.program = NcbiProgram.BLASTN
    self.megablast = True
    return self

  def unset_megablast(self) -> 'NcbiBlast':
    """
    Unsets the megablast option.

    Returns:
      'NcbiBlast': Returns self, part of the builder pattern.
    """
    self.megablast = False
    return self

  def set_database(self, database:NcbiDatabase) -> 'NcbiBlast':
    """
    Set the database for the search.

    Args:
      database (NcbiDatabase): An Ncbi database.

    Returns:
      'NcbiBlast': Returns self, part of the builder pattern.
    """
    self.database = database
    return self

  def build(self) -> 'NcbiBlast':
    """
    Builds a NcbiBlast object with all the information set.

    Returns:
      'NcbiBlast': A proper NCBI object.

    Throws:
      ValueError: Returns self, part of the builder pattern.
    """
    if not self.database:
      raise ValueError("No database specified")
    if self.megablast and self.program != NcbiProgram.BLASTN:
      raise ValueError("Megablast can only be set with blastn program")
    self.built = True
    return self

  def query(self, query:str) -> tuple[str, str]:
    """
    Submits a query to NCBI server and returns the job id and rtoe value.

    Args:
      query (str): A GI, Accession or sequence.

    Returns:
      tuple[str, str]: The RID (job id) and RTOE (estimated time to job
        completion)

    Throws:
      ValueError: If database is not set or not job data available.
      HTTPError: If request could not be processed.
    """
    if not self.database:
      raise ValueError("Database not set")
    pars = {
      "PROGRAM": self.program.value,
      "DATABASE": self.database.value,
      "CMD": "Put",
      "QUERY": query
    }
    if self.megablast:
      pars["MEGABLAST"] = "on"
    resp = requests.put(NcbiBlast.url, params=pars, timeout=120)
    resp.raise_for_status()
    job_data = get_qblast_info(resp)
    if not job_data:
      raise ValueError("There was no job data available in NCBI response")
    self.rid = job_data["RID"]
    self.last_response_time = time.time()
    return (job_data["RID"], job_data["RTOE"])

  @staticmethod
  def job_is_ready(rid:str) -> bool:
    """
    Check if a job is ready.

    Args:
      rid (str): The Job Id.

    Returns:
      bool: True is the job is ready.
    """
    pars = {
      "CMD": "Get",
      "FORMAT_OBJECT": "SearchInfo",
      "RID": rid
    }
    resp = requests.get(NcbiBlast.url, pars, timeout=120)
    job_data = get_qblast_info(resp)
    if not job_data:
      return False
    status_key, status_value = next(iter(job_data.items()))
    status_key = status_key.upper()
    status_value = status_value.upper()
    result = False
    if status_key == "STATUS" and status_value == "WAITING":
      result = False
    if status_key == "STATUS" and status_value == "UNKNOWN":
      result =  False
    if status_key == "STATUS" and status_value == "READY":
      result =  True
    if status_key == "THEREAREHITS" and status_value == 'YES':
      result =  True
    if status_key == "THEREAREHITS" and status_value == 'NO':
      result =  False
    return result

  def fetch_results(self) -> bool:
    """
    Fetch results of the complete job.
    Does not check that the result actually finished.

    Returns:
      bool: True if the request was succesful.
    """
    pars = {
      "CMD": "GET",
      "RID": self.rid,
      "FORMAT_TYPE": "JSON2"
    }
    resp = requests.get(
      NcbiBlast.url,
      params=pars,
      timeout=120
    )
    try:
      resp.raise_for_status()
    except requests.HTTPError:
      return False
    self.output_buffer = resp.content
    return True

  def wait_until_finnish(self, max_time:float=5) -> bool:
    """
    Waits Until the job is done or failed.
    Checks if the job completed every 60 seconds.

    Args:
      max_time (float): Max time of waiting, in minutes.

    Returns:
      bool: True if the job is complete. False is there was an error or the
        maximum waiting time is reached.
    """
    if not self.last_response_time or not self.rid:
      return False
    max_time = max_time * 60
    initial_time = self.last_response_time
    while True:
      current_time = time.time()
      if current_time - initial_time > max_time:
        return False
      next_time = self.last_response_time + 60.0 - current_time
      if next_time > 0:
        print(next_time)
        time.sleep(next_time)
      self.last_response_time = time.time()
      if NcbiBlast.job_is_ready(self.rid):
        return self.fetch_results()

  def get_output_buffer(self) -> bytes:
    """
    Returns the buffer with the downloaded output.

    Returns:
      bytes: The output buffer data if there is any.
    """
    if not self.output_buffer:
      return bytes()
    return self.output_buffer

  def write_results(self, outfile:str) -> int:
    """
    Writes output buffer to disk.

    Args:
      outfile (str): Output file to write.

    Throws:
      ValueError: If buffer is empty.
      OSError: If file is not writable.
    """
    if not self.output_buffer:
      raise ValueError("No data in output buffer")
    with open(outfile, 'wb') as f_out:
      return f_out.write(self.output_buffer)


@dataclass
class BlastHit:
  """
  Blast hit class. Contains information about individual blast hits results.
  """
  def __init__(self, hit_data: Dict):
    self.num = hit_data["num"]
    self.description = [
      BlastDescription(desc) for desc in hit_data["description"]
    ]
    self.len = hit_data["len"]
    self.hsps = [BlastHsp(hsp) for hsp in hit_data["hsps"]]

@dataclass
class BlastDescription:
  """
  Blast Description class. contains information about the a sequence in a
  blast hit.
  """
  def __init__(self, desc_data: Dict):
    self.identifier = desc_data["id"]
    self.accession = desc_data["accession"]
    self.title = desc_data["title"]
    self.taxid = desc_data["taxid"]
    self.sciname = desc_data["sciname"]

@dataclass
class BlastHsp:
  """
  Blast High Scoring Pair. Contains information about the exact match between
  the query sequence and the subject sequence.
  """
  #pylint: disable=too-many-instance-attributes
  def __init__(self, hsp_data: Dict):
    self.num = hsp_data["num"]
    self.bit_score = hsp_data["bit_score"]
    self.score = hsp_data["score"]
    self.evalue = hsp_data["evalue"]
    self.identity = hsp_data["identity"]
    self.query_from = hsp_data["query_from"]
    self.query_to = hsp_data["query_to"]
    self.query_strand = hsp_data["query_strand"]
    self.hit_from = hsp_data["hit_from"]
    self.hit_to = hsp_data["hit_to"]
    self.hit_strand = hsp_data["hit_strand"]
    self.align_len = hsp_data["align_len"]
    self.gaps = hsp_data["gaps"]
    self.qseq = hsp_data["qseq"]
    self.hseq = hsp_data["hseq"]
    self.midline = hsp_data["midline"]

@dataclass
class BlastStats:
  """
  Blast Stats class. Contains information about general statistics of a
  blast search.
  """
  def __init__(self, stats_data: Dict):
    self.db_num = stats_data["db_num"]
    self.db_len = stats_data["db_len"]
    self.hsp_len = stats_data["hsp_len"]
    self.eff_space = stats_data["eff_space"]
    self.kappa = stats_data["kappa"]
    self.lambda_ = stats_data["lambda"]
    self.entropy = stats_data["entropy"]

@dataclass
class BlastResults:
  """
  Blast Results class. Contains information about the results of a blast
  search, including statistics, hits and HSPs.
  """
  def __init__(self, search_data: Dict):
    self.query_id = search_data["query_id"]
    self.query_len = search_data["query_len"]
    self.hits = [BlastHit(hit) for hit in search_data["hits"]]
    self.stat = BlastStats(search_data["stat"])

@dataclass
class BlastParams:
  """
  Blast Parameters claass. Contains information about specific
  search parameters used in the blast search.
  """
  def __init__(self, params_data: Dict):
    self.expect = params_data["expect"]
    self.sc_match = params_data["sc_match"]
    self.sc_mismatch = params_data["sc_mismatch"]
    self.gap_open = params_data["gap_open"]
    self.gap_extend = params_data["gap_extend"]
    self.filter = params_data["filter"]

@dataclass
class BlastReport:
  """
  Blast Report class. Contains general information about the blast program and
  the database used for the blast search.
  """
  def __init__(self, report_data: Dict):
    self.program = report_data["program"]
    self.version = report_data["version"]
    self.reference = report_data["reference"]
    self.search_target = report_data["search_target"]
    self.params = BlastParams(report_data["params"])

@dataclass
class BlastOutput:
  """
  Blast output class. is the main class to navigate a blast output.
  """
  def __init__(
      self,
      report: BlastReport,
      params: BlastParams,
      results: BlastResults
    ):
    self.report = report
    self.params = params
    self.results = results

  @staticmethod
  def from_json(filename: str) -> 'BlastOutput':
    """
    Creates a blast output object from a json file.

    Args:
      filename (str): The input json file.

    Returns:
      BlastOutput2: A blast output object.
    """
    with open(filename, 'r', encoding="utf-8") as f_in:
      data = json.load(f_in)
      report_data = data['BlastOutput2']['report']
      params_data = report_data['params']
      results_data = report_data['results']['search']
      report = BlastReport(report_data)
      params = BlastParams(params_data)
      results = BlastResults(results_data)
      return BlastOutput(report, params, results)
