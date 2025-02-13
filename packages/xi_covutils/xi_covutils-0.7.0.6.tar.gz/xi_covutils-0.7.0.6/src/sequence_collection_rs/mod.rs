use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::exceptions::PyValueError;

#[pyclass]
#[derive(Clone, PartialEq, Debug)]
pub enum BioAlphabet {
  DNA = 0,
  RNA = 1,
  PROTEIN = 2,
  UNKNOWN = 3
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct BioSeq {
  identifier: String,
  sequence: String,
  alphabet: BioAlphabet
}

impl PartialEq for BioSeq {
  fn eq(&self, other: &Self) -> bool {
    self.identifier == other.identifier
      && self.sequence == other.sequence
      && self.alphabet == other.alphabet
  }
}

pub fn dna_to_rna(sequence: &str) -> String {
  sequence
    .chars()
    .map(
      |c| {
        match c {
          'T' => 'U',
          't' => 'u',
          _ => c
        }
      }
    )
    .collect()
}

pub fn rna_to_dna(sequence: &str) -> String {
  sequence
    .chars()
    .map(
      |c| {
        match c {
          'U' => 'T',
          'u' => 't',
          _ => c
        }
      }
    )
    .collect()
}

pub fn reverse_complement_rna(sequence: &str) -> String {
  dna_to_rna(&reverse_complement_dna(&rna_to_dna(sequence)))
}

pub fn reverse_complement_dna(sequence : &str) -> String {
  sequence
    .chars()
    .rev()
    .map(
      |c| {
        match c {
          'A' => 'T',
          'T' => 'A',
          'C' => 'G',
          'G' => 'C',
          'R' => 'Y',
          'Y' => 'R',
          'S' => 'S',
          'W' => 'W',
          'K' => 'M',
          'M' => 'K',
          'B' => 'V',
          'V' => 'B',
          'D' => 'H',
          'H' => 'D',
          'N' => 'N',
          'a' => 't',
          't' => 'a',
          'c' => 'g',
          'g' => 'c',
          'r' => 'y',
          'y' => 'r',
          's' => 's',
          'w' => 'w',
          'k' => 'm',
          'm' => 'k',
          'b' => 'v',
          'v' => 'b',
          'd' => 'h',
          'h' => 'd',
          'n' => 'n',
          _ => c
        }
      }
    )
    .collect()
}

#[pymethods]
impl BioSeq {
  #[new]
  fn new(
    identifier: String,
    sequence: String,
    alphabet: BioAlphabet
  ) -> Self {
    BioSeq {
      identifier,
      sequence,
      alphabet
    }
  }

  fn get_identifier(&self) -> &str {
    &self.identifier
  }

  fn get_sequence(&self) -> &str {
    &self.sequence
  }

  fn get_alphabet(&self) -> BioAlphabet {
    self.alphabet.clone()
  }

  fn __eq__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
    if let Ok(other) = other.extract::<PyRef<BioSeq>>() {
      Ok(other.eq(self))
    } else {
      Ok(false)
    }
  }

  #[staticmethod]
  fn unknown_bio_seq(identifier: String, sequence: String) -> Self {
    BioSeq {
      identifier,
      sequence,
      alphabet: BioAlphabet::UNKNOWN
    }
  }

  #[staticmethod]
  fn dna(sequence: String) -> Self {
    BioSeq {
      identifier: "".to_string(),
      sequence,
      alphabet: BioAlphabet::DNA
    }
  }

  #[staticmethod]
  fn rna(sequence: String) -> Self {
    BioSeq {
      identifier: "".to_string(),
      sequence,
      alphabet: BioAlphabet::RNA
    }
  }

  #[staticmethod]
  fn protein(sequence: String) -> Self {
    BioSeq {
      identifier: "".to_string(),
      sequence,
      alphabet: BioAlphabet::PROTEIN
    }
  }

  #[staticmethod]
  fn unknown(sequence: String) -> Self {
    BioSeq {
      identifier: "".to_string(),
      sequence,
      alphabet: BioAlphabet::UNKNOWN
    }
  }

  fn to_rna(&self) -> PyResult<BioSeq> {
    match self.alphabet {
      BioAlphabet::DNA => {
        Ok(
          BioSeq {
            identifier: self.identifier.clone(),
            sequence: dna_to_rna(&self.sequence),
            alphabet: BioAlphabet::RNA
          }
        )
      },
      BioAlphabet::RNA => Err(
        PyValueError::new_err(
          "RNA sequences cannot be converted to RNA."
        )
      ),
      BioAlphabet::PROTEIN => Err(
        PyValueError::new_err(
          "Protein sequences cannot be converted to RNA."
        )
      ),
      BioAlphabet::UNKNOWN => Err(
        PyValueError::new_err(
          "Unknown type sequences cannot be converted to RNA."
        )
      )
    }
  }

  fn to_dna(&self) -> PyResult<BioSeq> {
    match self.alphabet {
      BioAlphabet::DNA => Err(
        PyValueError::new_err(
          "DNA sequences cannot be converted to DNA."
        )
      ),
      BioAlphabet::RNA => {
        Ok(
          BioSeq {
            identifier: self.identifier.clone(),
            sequence: rna_to_dna(&self.sequence),
            alphabet: BioAlphabet::DNA
          }
        )
      },
      BioAlphabet::PROTEIN => Err(
        PyValueError::new_err(
          "Protein sequences cannot be converted to DNA."
        )
      ),
      BioAlphabet::UNKNOWN => Err(
        PyValueError::new_err(
          "Unknown type sequences cannot be converted to DNA."
        )
      )
    }
  }

  fn reverse_complement(&self) -> PyResult<BioSeq> {
    match self.alphabet {
      BioAlphabet::DNA => {
        Ok(
          BioSeq {
            identifier: self.identifier.clone(),
            sequence: reverse_complement_dna(&self.sequence),
            alphabet: self.alphabet.clone()
          }
        )
      },
      BioAlphabet::RNA => {
        Ok(
          BioSeq {
            identifier: self.identifier.clone(),
            sequence: reverse_complement_rna(&self.sequence),
            alphabet: self.alphabet.clone()
          }
        )
      },
      BioAlphabet::PROTEIN => Err(
        PyValueError::new_err(
          "Protein sequences cannot have reverse complement sequence."
        )
      ),
      BioAlphabet::UNKNOWN => Err(
        PyValueError::new_err(
          "Unknown type sequences cannot have reverse complement sequence."
        )
      )
    }
  }
}

#[pymodule]
pub fn sequence_collection_rs(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_class::<BioSeq>()?;
  m.add_class::<BioAlphabet>()?;
  Ok(())
}

#[cfg(test)]
mod test {

use super::*;

  #[test]
  fn test_dna_to_rna() {
    assert_eq!(dna_to_rna("ATCG"), "AUCG");
    assert_eq!(dna_to_rna("atcg"), "aucg");
  }

  #[test]
  fn test_rna_to_dna() {
    assert_eq!(rna_to_dna("AUCG"), "ATCG");
    assert_eq!(rna_to_dna("aucg"), "atcg");
  }

  #[test]
  fn test_reverse_complement_dna() {
    assert_eq!(reverse_complement_dna("ATCG"), "CGAT");
    assert_eq!(reverse_complement_dna("atcg"), "cgat");
  }

  #[test]
  fn test_reverse_complement_rna() {
    assert_eq!(reverse_complement_rna("AUCG"), "CGAU");
    assert_eq!(reverse_complement_rna("aucg"), "cgau");
  }

  #[test]
  fn test_bio_seq_eq() {
    let seq1 = BioSeq::new("seq1".to_string(), "ATCG".to_string(), BioAlphabet::DNA);
    let seq2 = BioSeq::new("seq1".to_string(), "ATCG".to_string(), BioAlphabet::DNA);
    let seq3 = BioSeq::new("seq1".to_string(), "ATCG".to_string(), BioAlphabet::DNA);
    let seq4 = BioSeq::new("seq1".to_string(), "CGAT".to_string(), BioAlphabet::DNA);
    let seq5 = BioSeq::new("seq1".to_string(), "ATCG".to_string(), BioAlphabet::RNA);
    let seq6 = BioSeq::new("seq1".to_string(), "ATCG".to_string(), BioAlphabet::PROTEIN);
    let seq7 = BioSeq::new("seq1".to_string(), "ATCG".to_string(), BioAlphabet::UNKNOWN);

    assert_eq!(seq1, seq2);
    assert_eq!(seq1, seq3);
    assert_ne!(seq1, seq4);
    assert_ne!(seq1, seq5);
    assert_ne!(seq1, seq6);
    assert_ne!(seq1, seq7);
  }

}