"""
Test Taxonomy Tree and classes.
"""
import os

import pandas as pd
from xi_covutils.taxonomy import TaxonomyTree, create_children_to_parent_mapping, create_names_to_taxid_mapping, create_taxid_to_names_mapping, get_species_level_taxids, read_taxonomy_names_dump_file


def test_get_children():
  """
  Tests get_children method of TaxonomyTree class.
  """
  mapping = {
    2:1, 3:1, 4:2, 5:2, 6:3, 7:3
  }
  tree = TaxonomyTree(mapping)
  children = tree.get_children(8)
  assert children == []
  children = tree.get_children(7)
  assert children == []
  children = tree.get_children(1)
  assert set(children) == {2, 3}
  children = tree.get_children(2)
  assert set(children) == {4, 5}

def test_get_subtree_nodes():
  """
  Tests get_subtree_nodes method of TaxonomyTree class.
  """
  mapping = {
    2:1, 3:1, 4:2, 5:2, 6:3, 7:3
  }
  tree = TaxonomyTree(mapping)
  children = tree.get_subtree_nodes(8)
  assert isinstance(children, list)
  assert not children
  children = tree.get_subtree_nodes(7)
  assert children == [7]
  children = tree.get_subtree_nodes(1)
  assert set(children) == {1, 2, 3, 4, 5, 6, 7}
  children = tree.get_subtree_nodes(2)
  assert set(children) == {2, 4, 5}

def test_retrieve_lineage():
  """
  Tests retriee_lineage method of TaxonomyTree class.
  """
  mapping = {
    4:2,2:1,3:1,1:1
  }
  tree = TaxonomyTree(mapping)
  parent = tree.get_parent(4)
  assert parent == (True, 2)
  parent = tree.get_parent(2)
  assert parent == (True, 1)
  lineage = tree.retrieve_lineage(4)
  assert lineage == [1, 2, 4]

def test_retrieve_truncated_lineage():
  """
  Tests retriee_truncated_lineage method of TaxonomyTree class.
  """
  mapping = {
    4:2,2:1,3:1,1:1,5:4, 6:5
  }
  tree = TaxonomyTree(mapping)
  lineage = tree.retrieve_truncated_lineage(6, 5)
  assert lineage == [1, 2, 4, 5, 6]
  lineage = tree.retrieve_truncated_lineage(6, 6)
  assert lineage == [1, 2, 4, 5, 6, 6]
  lineage = tree.retrieve_truncated_lineage(6, 4)
  assert lineage == [1, 2, 4, 5]

def test_common_lineage():
  """
  Tests common_lineage method of TaxonomyTree class.
  """
  mapping = {
    7:4,5:4,6:4,4:2,2:1,3:1,1:1
  }
  tree = TaxonomyTree(mapping)
  clin = tree.common_lineage([])
  assert clin == []
  clin = tree.common_lineage([4])
  assert clin == [1, 2, 4]
  clin = tree.common_lineage([5,6])
  assert clin == [1, 2, 4]
  clin = tree.common_lineage([5,6,7])
  assert clin == [1, 2, 4]
  clin = tree.common_lineage([5,6,7,3])
  assert clin == [1]

def test_read_taxonomy_names_dump_file(test_data_folder):
  """ Test reading the taxonomy names dump file"""
  outfile = os.path.join(
    test_data_folder,
    "names_example.dmp"
  )
  names = read_taxonomy_names_dump_file(outfile)
  assert isinstance(names, pd.DataFrame)
  assert names.shape == (30, 4)
  assert names.columns.to_list() == [
    "taxid",
    "name",
    "unique_name",
    "category_name"
  ]

def test_create_names_to_taxid_mapping(test_data_folder):
  """ Test create names to taxid mapping creation"""
  names_file = os.path.join(
    test_data_folder,
    "names_example.dmp"
  )
  expected = {
    "all": 1,
    "root": 1,
    "Bacteria": 2,
    "bacteria": 2,
    "eubacteria": 2,
    "Monera": 2,
    "Procaryotae": 2,
    "Prokaryotae": 2,
    "Prokaryota": 2,
    "prokaryote": 2,
    "prokaryotes": 2,
    "Azorhizobium Dreyfus et al. 1988 emend. Lang et al. 2013": 6,
    "Azorhizobium": 6,
    "ATCC 43989": 7,
    "Azorhizobium caulinodans Dreyfus et al. 1988": 7,
    "Azorhizobium caulinodans": 7,
    "Azotirhizobium caulinodans": 7,
    "CCUG 26647": 7,
    "DSM 5975": 7,
    "IFO 14845": 7,
    "JCM 20966": 7,
    "LMG 6465": 7,
    "LMG:6465": 7,
    "NBRC 14845": 7,
    "ORS 571": 7,
    "Acyrthosiphon pisum symbiont P": 9,
    "Buchnera aphidicola Munson et al. 1991": 9,
    "Buchnera aphidicola": 9,
    "primary endosymbiont of Schizaphis graminum": 9,
    "strain Sg (ex Schizaphis graminum)": 9,
    "Bacteria <bacteria>": 2,
    "Monera <bacteria>": 2,
    "Procaryotae <bacteria>": 2,
    "Prokaryotae <bacteria>": 2,
    "Prokaryota <bacteria>": 2,
    "prokaryote <bacteria>": 2,
    "prokaryotes <bacteria>": 2,
    "ATCC 43989 <type strain>": 7,
    "CCUG 26647 <type strain>": 7,
    "DSM 5975 <type strain>": 7,
    "IFO 14845 <type strain>": 7,
    "JCM 20966 <type strain>": 7,
    "LMG 6465 <type strain>": 7,
    "LMG:6465 <type strain>": 7,
    "NBRC 14845 <type strain>": 7,
    "ORS 571 <type strain>": 7,
    "strain Sg (ex Schizaphis graminum) <type strain>": 9,
  }
  mapping = create_names_to_taxid_mapping(names_file)
  assert mapping == expected

def test_create_taxid_to_names_mapping(test_data_folder):
  """ Test create taxid to names mapping creation """
  names_dump_file = os.path.join(test_data_folder, "names_example.dmp")
  mapping = create_taxid_to_names_mapping(names_dump_file)
  expected = {
    1: "root",
    2: "Bacteria",
    6: "Azorhizobium",
    7: "Azorhizobium caulinodans",
    9: "Buchnera aphidicola",
  }
  assert mapping == expected

def test_get_species_level_taxids(test_data_folder):
  """ Test retrieve species level taxids """
  nodes_files = os.path.join(test_data_folder, "nodes_example.dmp")
  spec_taxids = set(get_species_level_taxids(nodes_files))
  expected = set([7, 9, 11, 14, 17, 19, 21])
  assert spec_taxids == expected

def test_create_children_to_parent_mapping(test_data_folder):
  """ Test create children to parent mapping """
  nodes_files = os.path.join(test_data_folder, "nodes_example.dmp")
  mapping = create_children_to_parent_mapping(nodes_files)
  expected = {
    1: 1,
    2: 131567,
    6: 335928,
    7: 6,
    9: 32199,
    10: 1706371,
    11: 1707,
    13: 203488,
    14: 13,
    16: 32011,
    17: 16,
    18: 213421,
    19: 2812025,
    20: 76892,
    21: 20,
  }
  assert mapping == expected
