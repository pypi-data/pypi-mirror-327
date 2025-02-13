"""
  Run mkdssp to get secondary structure information from a pdb.

  Structure one letter code.
  G = 3-turn helix (310 helix). Min length 3 residues.
  H = 4-turn helix (α helix). Minimum length 4 residues.
  I = 5-turn helix (π helix). Minimum length 5 residues.
  T = hydrogen bonded turn (3, 4 or 5 turn)
  E = extended strand in parallel and/or anti-parallel β-sheet conformation.
      Min length 2 residues.
  B = residue in isolated β-bridge (single pair β-sheet hydrogen bond formation)
  S = bend (the only non-hydrogen-bond based assignment).
  C = coil (residues which are not in any of the above conformations).

"""
from os import environ
from os.path import exists
from subprocess import check_output
from shutil import which
import re
from typing import Any, Optional

MKDSSP_LINE_PATTERN = re.compile(
  "^(?P<index>.....)" # DSSP residue number
  "(?P<pdb_num>......)" # PDB residue number
  "(?P<pdb_chain>..)" # chain
  "(?P<aa>...)" # Aminoacid
  "(?P<structure>.)" # Structure
  "(?P<st_desc>........)" # Addiotional structure descriptions
  "(?P<BP1>....)" # Bridge pair candidate 1
  "(?P<BP2>....)" # Bridge pair candidate 2
  "(?P<acc>.....)" # Solvent accesibility
  "(?P<hb1>............)" # Hidrogen bond pair 1
  "(?P<hb2>...........)" # Hidrogen bond pair 2
  "(?P<hb3>...........)" # Hidrogen bond pair 3
  "(?P<hb4>...........)" # Hidrogen bond pair 4
  "(?P<tco>........)" # TCO, cosino of C=O angles between two adjacent residues.
  "(?P<kappa>......)" # Kappa: the virtual bond angle.
  "(?P<alpha>......)" # Some value named alpha.
  "(?P<phi>......)" # Dihedral phi angle
  "(?P<psi>......)" # Dihedral psi angle
  "(?P<xca>.......)" # Alpha carbon x coordinate
  "(?P<yca>.......)" # Alpha carbon y coordinate
  "(?P<zca>.......)" # Alpha carbon z coordinate
  "(?P<chain>.................)?" # Chain
  "(?P<autochain>..........)?" # Autochain
  "$" # End of line
)

def _get_mkdssp_exec():
  if "MKDSSP_PATH" in environ and exists(environ["MKDSSP_PATH"]):
    return environ["MKDSSP_PATH"]
  mk_dssp = which("mkdssp")
  if mk_dssp:
    return mk_dssp
  raise(ValueError(
    "mkdssp program should be on path or MKDSSP_PATH"+
    "enviromental variable should be set."))

def _parse_mkdssp_line(line:str) -> Optional[dict[str, Any]]:
  c_match = re.match(MKDSSP_LINE_PATTERN, line)
  if c_match:
    try:
      pdb_num = int(c_match.group('pdb_num').strip())
    except ValueError:
      return None
    chain = str(c_match.group('pdb_chain').strip())
    return {
      'chain': chain,
      'pdb_num': pdb_num,
      'index': int(c_match.group('index').strip()),
      'aa': c_match.group('aa').strip(),
      'structure': c_match.group('structure').strip()
    }
  return None

def _parse_mkdssp_output(
    content:bytes
  ) -> dict[tuple[str, int], dict[str, Any]]:
  decoded = content.decode().split("\n")
  results = {}
  in_data_section = False
  for line in decoded:
    if in_data_section:
      parsed = _parse_mkdssp_line(line)
      if parsed:
        chain = str(parsed['chain'])
        pdb_num = int(parsed['pdb_num'])
        results[(chain, pdb_num)] = parsed
    else:
      in_data_section = in_data_section or line.startswith("  #  RESIDUE")
  return results

def mkdssp(pdb_file:str) -> dict[tuple[str, int], dict[str, Any]]:
  """
  Run mkdssp program.

  Args:
    pdb_file (str): the path of the input pdb file.

  Returns:
    str: The output of the mkdssp program.
  """
  mk_dssp = _get_mkdssp_exec()
  cmd = [mk_dssp, '--output-format', 'dssp', '-i', pdb_file]
  output = check_output(cmd)
  return _parse_mkdssp_output(output)
