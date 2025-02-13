use pyo3::prelude::*;
use pyo3::wrap_pymodule;

mod clustering_rs;
mod distances_rs;
mod sequence_collection_rs;

#[pymodule]
fn rs_covutils(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
	m.add_wrapped(wrap_pymodule!(clustering_rs::clustering_rs))?;
	m.add_wrapped(wrap_pymodule!(distances_rs::distances_rs))?;
	m.add_wrapped(wrap_pymodule!(sequence_collection_rs::sequence_collection_rs))?;
	Ok(())
}
