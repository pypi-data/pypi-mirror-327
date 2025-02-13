use std::f64::EPSILON;

use pyo3::{
  pyfunction, pymodule, types::PyModule, wrap_pyfunction, Bound, PyResult, Python
};

#[pyfunction]
pub fn js_distance(prob_p: Vec<f64>, prob_q: Vec<f64>) -> f64 {
  jensen_shannon_distance(&prob_p, &prob_q)
}

pub fn jensen_shannon_distance(prop_p: &[f64], prob_q: &[f64]) -> f64 {
  // Normalize probabilities
  let p_sum = prop_p.iter().fold(0.0, |x, y| x + y);
  let q_sum = prob_q.iter().fold(0.0, |x, y| x + y);
  let p_norm = prop_p.iter().map(|x| x / p_sum).collect::<Vec<_>>();
  let q_norm = prob_q.iter().map(|x| x / q_sum).collect::<Vec<_>>();
  // Compute average distribution
  let m = p_norm
    .iter()
    .zip(q_norm.iter())
    .map(|(a, b)| 0.5 as f64 * (a+b))
    .collect::<Vec<_>>();
  // Calculate Jensen-Shannon divergence components
  let p_js = kullback_leibler_divergence(&p_norm, &m);
  let q_js = kullback_leibler_divergence(&q_norm, &m);
  // Calculate Jensen-Shannon distance
  let js_distance = 0.5 * (p_js + q_js);
  js_distance
}

#[pyfunction]
pub fn kl_divergence(prob_p: Vec<f64>, prob_q: Vec<f64>) -> f64 {
  kullback_leibler_divergence(&prob_p, &prob_q)
}

pub fn kullback_leibler_divergence(prob_p: &[f64], prob_q: &[f64]) -> f64 {
  let kl_div = prob_p
    .iter()
    .zip(prob_q.iter())
    .fold(
      0.0,
      |acc, (&x, &y)| {
        if x > EPSILON && y > EPSILON {
          acc + x * ((x / y).ln())
        } else {
          acc
        }
    }
  );
  kl_div
}

#[pymodule]
pub fn distances_rs(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_function(wrap_pyfunction!(kl_divergence, m)?)?;
  m.add_function(wrap_pyfunction!(js_distance, m)?)?;
  Ok(())
}