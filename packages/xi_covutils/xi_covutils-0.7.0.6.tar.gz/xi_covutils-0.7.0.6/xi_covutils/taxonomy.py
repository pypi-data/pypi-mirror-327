"""
Taxonomy module

Function and classes to work with taxonomy.
"""
from collections import defaultdict
from functools import reduce
from typing import Optional, cast

import pandas as pd

class TaxonomyTree:
  """
  Taxonomy Tree class.
  """
  def __init__(self, children_to_parent_mapping:dict[int, int]):
    self.mapping = children_to_parent_mapping
    self.reverse_mapping = self._build_reverse_mapping(self.mapping)

  @staticmethod
  def _build_reverse_mapping(mapping:dict[int, int]) -> dict[int, list[int]]:
    result = defaultdict(list[int])
    for child, parent in mapping.items():
      result[parent].append(child)
    return result

  def get_parent(self, taxid:int) -> tuple[bool, Optional[int]]:
    """
    Get the parent of a Node.

    Args:
      taxid (int): A taxid.

    Returns:
      tuple[bool, Optional[int]]: If given taxid is in the taxonomy tree.
        The first value is True. If the given node has a parent return its
        taxid, if the node is the root, i.e. do no have a parent, returns None.
    """
    parent = self.mapping.get(taxid)
    if parent is None:
      return (False, None)
    if parent == taxid:
      return (True, None)
    return (True, parent)

  def valid_taxid(self, taxid:int) -> bool:
    """
    Checks if a given taxid, belongs to the Taxonomy Tree.

    Args:
      taxid (int): A taxid.

    Returns:
      bool: True if the given taxid is in the Taxonomy Tree.
    """
    return taxid in self.mapping or taxid in self.mapping.values()

  def is_parent(self, taxid:int) -> bool:
    """
    Checks if a given taxid, is a parent of another node in the
    Taxonomy Tree.

    Args:
      taxid (int): A taxid.

    Returns:
      bool: True if the given taxid is a parent node.
    """
    return taxid in self.mapping

  def retrieve_truncated_lineage(
    self,
    taxid:int,
    lineage_length:int=6,
    fill_incomplete:bool=True
  ) -> list[int]:
    """
    Retrieves a truncated lineage from the root to the given taxid.
    """
    full_lineage = self.retrieve_lineage(taxid)
    partial_lineage = full_lineage[:lineage_length]
    if fill_incomplete and len(partial_lineage) < lineage_length:
      partial_lineage.extend(
        [partial_lineage[-1]] * (lineage_length-len(partial_lineage))
      )
    return partial_lineage

  def retrieve_lineage(self, taxid:int) -> list[int]:
    """
    Retrieves the complete lineage from the root to the given
    taxid.

    Args:
      taxid (int): A taxid.

    Returns:
      list[int]: A list of taxids representing the complete lineage.
    """
    lineage = [taxid]
    node = taxid
    while True:
      parent, child = self.get_parent(node)
      if not parent:
        break
      if not child:
        break
      lineage.insert(0, child)
      node = child
    return lineage

  def common_lineage(self, taxids:list[int]) -> list[int]:
    """
    Gets the common lineage from the root for a group of nodes.

    Args:
      taxids (list[int]): A groups of nodes taxids.

    Returns:
      list[int]: The common lineage of all given nodes.
    """
    def _max_common_lineage(lin1: list[int], lin2:list[int]) -> list[int]:
      if lin1 == []:
        return lin2
      if lin2 == []:
        return lin1
      return [
        a
        for a, b in zip(lin1, lin2)
        if a == b
      ]
    all_lineages = [
      self.retrieve_lineage(node)
      for node in taxids
    ]
    return reduce(_max_common_lineage, all_lineages, [])

  def get_children(self, taxid:int) -> list[int]:
    """
    Get the children nodes of a given node in the Taxonomy Tree.

    Args:
      taxid (int): A taxid Node.

    Returns:
      list[int]: A list of the children nodes.
    """
    return self.reverse_mapping.get(taxid, [])

  def get_subtree_nodes(self, taxid:int) -> list[int]:
    """
    Gets all nodes in a subtree starting from a given node including the node
    itself.

    Args:
      taxid (int): A taxid Node.

    Returns:
      list[int]: A list of the children Nodes.
    """
    result = []
    to_visit = [taxid]
    while to_visit:
      c_id = to_visit.pop()
      if not self.valid_taxid(c_id):
        continue
      result.append(c_id)
      c_children = self.get_children(c_id)
      for child in c_children:
        if not child in result:
          to_visit.append(child)
    return result

  def lineage_contains(self, query: int, subject:set[int]) -> Optional[int]:
    """
    Check if the lineage of a taxid contains any of the given suject taxids.
    Checks from terminal leaf to root of the lineage. The first element that
    is in subject is returned.

    Args:
      query (int): a Query Tax Id.
      subject (set[int]): A set of taxids.

    Returns:
      Optional[int]: A first taxid in the lineage that is found in subject.
    """
    lineage = self.retrieve_lineage(query)
    for c_id in reversed(lineage):
      if c_id in subject:
        return c_id
    return None

def create_children_to_parent_mapping(
    taxonomy_nodes_file:str
  ) -> dict[int, int]:
  """
  Create a dictionary mapping children taxids to their parents
  reading a NCBI taxonomy nodes dump file.
  Processing this file can be time consuming, is better to cache this function
  results to reuse it.

  https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz

  Args:
    taxonomy_nodes_file (str): the path to the taxonomy nodes dump file.

  Returns:
    dict[int, int]: A dict from child taxids to their parents.
  """
  mapping = (
    pd
      .read_csv(
        taxonomy_nodes_file,
        sep="\t",
        header = None
      )
      .iloc[:, [0, 2]]
      .rename(
        columns={0:"taxid", 2:"parent"}
      )
      .set_index(
        "taxid"
      )
      ["parent"]
      .to_dict()
  )
  mapping = cast(dict[int, int], mapping)
  return mapping

def get_species_level_taxids(
    taxonomy_nodes_file: str
  ) -> list[int]:
  """
  Retrieves all taxids from species level taxonomy
  reading a NCBI taxonomy nodes dump file.
  Processing this file can be time consuming, is better to cache this function
  results to reuse it.

  https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz

  Args:
    taxonomy_nodes_file (str): the path to the taxonomy nodes dump file.

  Returns:
    list[int]: A list with all species level taxids.
  """
  species = (
    pd
      .read_csv(
        taxonomy_nodes_file,
        sep="\t",
        header=None
      )
      .iloc[:, [0, 4]]
      .rename(
        columns = {0:"taxid", 4:"rank"}
      )
      .query("rank=='species'")
      .taxid
      .to_list()
  )
  return species

def read_taxonomy_names_dump_file(
    taxonomy_namesdump_file:str
  ) -> pd.DataFrame:
  """
  Read the taxonomy names dump file into Pandas DataFrame.

  Args:
    taxonomy_namesdump_file (str): The taxonomy dump file.

  Returns:
    pd.DataFrame: A pandas DataFrame
  """
  data = (
    pd.read_csv(
      taxonomy_namesdump_file,
      sep="\t",
      header=None
    )
    .drop([1, 3, 5, 7], axis=1)
    .rename(
      columns={
        0:"taxid",
        2:"name",
        4:"unique_name",
        6:"category_name"
      }
    )
  )
  return data

def create_names_to_taxid_mapping(
    taxonomy_namesdump_file:str
  ) -> dict[str, int]:
  """
  Generates a mappping from names, and unique names to the taxid.
  Reads the NCBI taxonomy names dump file.
  Processing this file can be time consuming, is better to cache this function
  results to reuse it.

  https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz

  Returns:
    dict[str, int]: The mapping from names and unique names to taxid.
  """
  result:dict[str, int] = {}
  data = read_taxonomy_names_dump_file(taxonomy_namesdump_file)
  for _, row in data.iterrows():
    taxid:int = int(row["taxid"])
    name:str = str(row["name"])
    unique:str = str(row["unique_name"])
    if name != 'nan':
      result[name] = taxid
    if unique != 'nan':
      result[unique] = taxid
  return result

def create_taxid_to_names_mapping(
    taxonomy_namesdump_file:str
  ) -> dict[int, str]:
  """
  Generates a mappping from taxid to scientific names.
  Reads the NCBI taxonomy names dump file.
  Processing this file can be time consuming, is better to cache this function
  results to reuse it.

  https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz

  Returns:
    dict[int, str]: The mapping from taxid to scientific names.
  """
  result:dict[int, str] = {}
  data = read_taxonomy_names_dump_file(taxonomy_namesdump_file)
  for _, row in data.iterrows():
    if row["category_name"] != "scientific name":
      continue
    taxid:int = int(row["taxid"])
    name:str = str(row["name"])
    result[taxid] = name
  return result

def replace_taxids_with_names(
  taxids:list[int],
  taxid_to_names_map:dict[int, str]
) -> list[str]:
  """
  Replaces a list of taxids with their scientific names using the providing
  mapping.
  """
  return [taxid_to_names_map[taxid] for taxid in taxids]
