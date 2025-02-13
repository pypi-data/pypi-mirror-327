use crate::distances_rs::jensen_shannon_distance;
use std::collections::{HashMap, HashSet};
use std::mem::replace;
use pyo3::prelude::*;

#[pyclass]
pub struct IdentityCalculator { }

impl IdentityCalculator {
  fn _identity_fraction(&self, s1: &String, s2: &String) -> Option<f64> {
    let l1 = s1.len();
    let l2 = s2.len();
    if l1 != l2 {
      return None;
    };
    let mut identical:i32 = 0;
    let mut total:i32 = 0;
    for (c1, c2) in s1.chars().zip(s2.chars()) {
      if !((c1 == '-' || c1 == '_') && (c2=='-' || c2=='_')) {
        total = total + 1;
        identical = identical + (c1==c2) as i32;
      }
    };
    Some((identical as f64) / (total as f64))
  }
}

#[pymethods]
impl IdentityCalculator {
  #[new]
  pub fn new() -> IdentityCalculator {
    IdentityCalculator {}
  }
  pub fn identity_fraction(&self, s1: String, s2:String) -> Option<f64> {
    self._identity_fraction(&s1, &s2)
  }
}


/// The `Gapstripper` struct provides methods for stripping gaps from sequences.
#[pyclass]
pub struct Gapstripper { }

impl Gapstripper {
  fn _template(&self, sequences: &Vec<String>, use_reference:bool) -> Vec<bool> {
    match use_reference {
      true => {
        sequences[0]
          .clone()
          .chars()
          .map(|c| c == '-')
          .collect()
      },
      false => {
        let templates =
          sequences
            .iter()
            .map(
              |seq|
                seq
                  .clone()
                  .chars()
                  .map(|c| c == '-')
                  .collect::<Vec<_>>()
              )
            .collect::<Vec<_>>();
        let mut template = vec![true; templates[0].len()];
        for temp in &templates {
          template = temp
            .iter()
            .zip(&template)
            .map(|(x, y)| *x && *y)
            .collect();
        }
        template
      }
    }
  }
  fn _gapstrip_sequences(
    &self,
    sequences: &Vec<String>,
    use_reference:bool
  ) -> Vec<String> {
    let template = self._template(&sequences, use_reference);
    sequences
      .iter()
      .map(|seq| {
        seq.chars()
          .zip(&template)
          .filter(|(_, t)| !**t)
          .map(|(c, _)| c)
          .collect::<String>()
      })
      .collect::<Vec<_>>()
  }
}


#[pymethods]
impl Gapstripper {
  /// Creates a new `Gapstripper` instance.
  #[new]
  pub fn new() -> Gapstripper {
    Gapstripper {}
  }

  /// Strips gaps from a single sequence.
  ///
  /// # Arguments
  ///
  /// * `sequence` - The input sequence.
  ///
  /// # Returns
  ///
  /// The sequence with gaps removed.
  pub fn gapstrip_sequence(&self, sequence: String) -> String {
    let mut stripped = String::new();
    for c in sequence.chars() {
      if c != '-' {
        stripped.push(c);
      }
    }
    stripped
  }

  /// Strips gaps from multiple sequences.
  ///
  /// # Arguments
  ///
  /// * `sequences` - The input sequences.
  ///
  /// # Returns
  ///
  /// The sequences with gaps removed.
  ///
  /// # Example
  ///
  /// ```
  /// use clustering_rs::Gapstripper;
  ///
  /// let gapstripper = Gapstripper::new();
  /// let sequences = vec![
  ///     String::from("AT-GC"),
  ///     String::from("A--TGC"),
  ///     String::from("ATCG-"),
  /// ];
  /// let stripped_sequences = gapstripper.gapstrip_sequences(sequences);
  ///
  /// assert_eq!(stripped_sequences, vec![
  ///     String::from("ATGC"),
  ///     String::from("ATGC"),
  ///     String::from("ATCG"),
  /// ]);
  /// ```
  pub fn gapstrip_sequences(
    &self,
    sequences: Vec<String>,
    use_reference:bool
  ) -> Vec<String> {
    self._gapstrip_sequences(&sequences, use_reference)
  }
}

// Simple class to represent sequence clusters.
#[pyclass]
#[derive(Debug, Clone)]
pub struct Cluster {
  #[pyo3(get, set)]
  pub representative: Option<String>,
  #[pyo3(get, set)]
  pub representative_index: Option<i32>,
  #[pyo3(get, set)]
  pub sequences: Vec<String>,
  #[pyo3(get, set)]
  pub indexes: Vec<i32>,
  #[pyo3(get, set)]
  pub nseq: i32
}

#[pymethods]
impl Cluster {
  #[new]
  pub fn new() -> Cluster {
    Cluster {
      representative: None,
      representative_index: None,
      sequences: Vec::new(),
      indexes: Vec::new(),
      nseq: 0
    }
  }
  pub fn __repr__(&self) -> String {
    format!(
      "Cluster: [{:?}] [{:?}] {:?}",
      self.nseq,
      self.representative,
      self.sequences
    )
  }

  pub fn add(&mut self, seq:String, index:i32) {
    self.sequences.push(seq);
    self.indexes.push(index);
    self.nseq += 1;
  }
}

impl From<(&String, i32)> for Cluster {
  fn from((seq, index): (&String, i32)) -> Self {
    let mut cluster = Cluster::new();
    cluster.representative = Some(seq.clone());
    cluster.representative_index = Some(index);
    cluster.sequences.push(seq.clone());
    cluster.indexes.push(index);
    cluster.nseq = 1;
    cluster
  }
}

impl From<Vec<(String, i32)>> for Cluster {
  fn from(sequences: Vec<(String, i32)>) -> Self {
    let mut cluster = Cluster::new();
    for (i, (seq, index)) in sequences.into_iter().enumerate() {
      if i == 0 {
        cluster.representative = Some(seq.clone());
        cluster.representative_index = Some(index);
      }
      cluster.add(seq, index);
    }
    cluster
  }
}

#[pyclass]
pub struct Hobohm1 {
  pub sequences: Vec<String>,
  pub identity_cutoff: f64,
  pub max_clusters: f64
}

#[pymethods]
impl Hobohm1 {
  #[new]
  pub fn new() -> Hobohm1 {
    Hobohm1 {
      sequences: Vec::new(),
      identity_cutoff: 0.62,
      max_clusters: f64::INFINITY
    }
  }
  pub fn with_cutoff(&mut self, cutoff: f64) {
    self.identity_cutoff = cutoff;
  }
  pub fn with_max_clusters(&mut self, max_clusters: f64) {
    self.max_clusters = max_clusters;
  }
  pub fn with_sequences(&mut self, sequences: Vec<String>) {
    self.sequences = sequences;
  }
  pub fn get_clusters(&self) -> Vec<Cluster> {
    let mut select: Vec<Cluster> = Vec::new();
    let gapstripper = Gapstripper::new();
    let sequences = gapstripper
      ._gapstrip_sequences(&self.sequences, false);
    let id_calc = IdentityCalculator::new();
    for (i, seq) in sequences.into_iter().enumerate() {
      let mut add_to_cluster : Option<&mut Cluster> = None;
      for clu in &mut select {
        let representative = clu.representative.as_ref();
        if representative.is_none() {
          continue;
        }
        let identity = id_calc
          ._identity_fraction(&seq, representative.unwrap());
        if identity.is_some() && identity.unwrap() >= self.identity_cutoff {
          add_to_cluster = Some(clu);
          break;
        }
      }
      match add_to_cluster.as_mut() {
        None => {
          let mut cluster = Cluster::new();
          cluster.representative = Some(seq.clone());
          cluster.representative_index = Some(i as i32);
          cluster.sequences.push(seq);
          cluster.indexes.push(i as i32);
          cluster.nseq = 1;
          select.push(cluster);
        },
        Some(cluster) => {
          cluster.add(seq, i as i32);
        }
      }
      if select.len() >= self.max_clusters as usize {
        break;
      }
    }
    select
  }
}

#[pyclass]
pub struct KmerClustering {
  pub kmer_length: usize,
  pub distance_cutoff: f64,
  pub seq_map: Vec<HashMap<String, usize>>,
  pub clusters: Vec<Cluster>
}

impl KmerClustering {
  pub fn build_kmers(
    sequence: &String,
    kmer_size: usize
  ) -> HashMap<String, usize> {
    let start_indexes = 0..(sequence.len()-kmer_size+1);
    let kmers = start_indexes
      .map(|i| { sequence[i..i+kmer_size].to_string() })
      .collect::<Vec<_>>();
    let mut counts : HashMap<String, usize> = HashMap::new();
    for kmer in kmers {
      let count = counts
        .entry(kmer)
        .or_insert(0);
      *count += 1;
    };
    counts
  }
  fn build_seqmap(&mut self, sequences: &Vec<String>) {
    self.seq_map = sequences
      .iter()
      .map(
        | s|
          KmerClustering::build_kmers(s, self.kmer_length)
      )
      .collect::<Vec<_>>();
  }
  fn kmer_count_distance(
    kmer_count1: &HashMap<String, usize>,
    kmer_count2: &HashMap<String, usize>
  ) -> f64 {
    let all_kmers = kmer_count1
      .keys()
      .chain(kmer_count2.keys())
      .collect::<HashSet<_>>();
    let p1 = all_kmers
      .iter()
      .map(|k| (*kmer_count1.get(*k).unwrap_or(&0)) as f64)
      .collect::<Vec<_>>();
    let p2 = all_kmers
      .iter()
      .map(|k| (*kmer_count2.get(*k).unwrap_or(&0)) as f64)
      .collect::<Vec<_>>();
    let js_distance = jensen_shannon_distance(&p1, &p2);
    js_distance
  }
  pub fn closest(
    &self,
    kmers_count: &HashMap<String, usize>,
    clusters: &Vec<Cluster>
  ) -> Option<(usize, f64)> {
    let mut min_index = None;
    let mut min_distance = f64::INFINITY;
    for (i, cluster) in clusters.iter().enumerate() {
      for seq_index in cluster.indexes.iter() {
        let seq_kmers = {
          &self.seq_map[*seq_index as usize]
        };
        let distance = KmerClustering::kmer_count_distance(
          &kmers_count,
          &seq_kmers
        );
        if distance < min_distance {
          min_distance = distance;
          min_index = Some(i);
        }
      }
    }
    min_index.map(|i| (i, min_distance))
  }
}

#[pymethods]
impl KmerClustering {
  #[new]
  pub fn new() -> KmerClustering {
    KmerClustering {
      kmer_length: 3,
      distance_cutoff: 0.05,
      seq_map: vec![],
      clusters: Vec::new()
    }
  }
  pub fn with_kmer_length(&mut self, kmer_length: usize) {
    self.kmer_length = kmer_length;
  }
  pub fn with_cutoff(&mut self, cutoff: f64) {
    self.distance_cutoff = cutoff;
  }
  pub fn compute_clusters(&mut self, sequences: Vec<String>) {
    self.build_seqmap(&sequences);
    let mut clusters = Vec::new();
    for (i, kmers) in self.seq_map.iter().enumerate() {
      let mut cluster_to_grow = None;
      let closest = self.closest(kmers, &clusters);
      match closest{
        None => {},
        Some((closest_index, distance)) => {
          if distance < self.distance_cutoff {
            cluster_to_grow = Some(closest_index);
          }
        }
      }
      match cluster_to_grow {
        None => {
          clusters
            .push(Cluster::from((&sequences[i], i as i32)));
        },
        Some(closest_index) => {
          clusters[closest_index]
            .add(sequences[i].clone(), i as i32);
        }
      }
    }
    self.clusters = clusters.clone();
  }
  pub fn get_clusters(&mut self) -> Vec<Cluster> {
    self.clusters.clone()
  }
  pub fn take_clusters(&mut self) -> Vec<Cluster> {
    replace(&mut self.clusters, vec![])
  }
}

#[pymodule]
pub fn clustering_rs(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_class::<IdentityCalculator>()?;
  m.add_class::<Gapstripper>()?;
  m.add_class::<Hobohm1>()?;
  m.add_class::<Cluster>()?;
  m.add_class::<KmerClustering>()?;
  Ok(())
}

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn it_works() {
    let i = IdentityCalculator{};
    let v = i.identity_fraction(
      String::from("ACTGACTG"),
      String::from("ACTGACTA")
    );
    assert_eq!(v, Some(7 as f64/8 as f64));
  }

  #[test]
  fn test_gapstripper_without_reference() {
    let gapstripper = Gapstripper::new();
    let sequences = vec![
        String::from("AT--GC"),
        String::from("A--TGC"),
        String::from("AT-G--"),
    ];
    let stripped_sequences = gapstripper
      .gapstrip_sequences(sequences, false);
    assert_eq!(stripped_sequences, vec![
        String::from("AT-GC"),
        String::from("A-TGC"),
        String::from("ATG--"),
    ]);
  }
  #[test]
  fn test_gapstripper_with_reference() {
    let gapstripper = Gapstripper::new();
    let sequences = vec![
        String::from("AT--GC"),
        String::from("A--TGC"),
        String::from("AT-G--"),
    ];
    let stripped_sequences = gapstripper
      .gapstrip_sequences(sequences, true);
    assert_eq!(stripped_sequences, vec![
        String::from("ATGC"),
        String::from("A-GC"),
        String::from("AT--"),
    ]);
  }
  #[test]
  fn test_hobohm1(){
    let mut hobohm1 = Hobohm1::new();
    let sequences = vec![
      String::from("ATGCCTACTGACTGACTACT"),
      String::from("ATGCCTACTGACTGACTACA"),
      String::from("TGCCTACTGACTGACTACAA"),
      String::from("TGCCTACTGACTGACTACAG")
    ];
    hobohm1.with_cutoff(0.8);
    hobohm1.with_max_clusters(2.0);
    hobohm1.with_sequences(sequences);
    let clusters = hobohm1.get_clusters();
    assert_eq!(clusters.len(), 2);
  }
  #[test]
  fn test_kmer_clustering(){
    let mut kmer_clustering = KmerClustering::new();
    let sequences = vec![
      String::from("ATGCCTACTGACTGACTACT"),
      String::from("ATGCCTACTGACTGACTACA"),
      String::from("TGCTATGATGCTCATACTCT"),
      String::from("TGCTATGATGCTCATACTCT")
    ];
    kmer_clustering.with_cutoff(0.03);
    kmer_clustering.with_kmer_length(3);
    kmer_clustering.compute_clusters(sequences);
    let clusters = kmer_clustering.get_clusters();
    assert_eq!(clusters.len(), 2);
  }
}
