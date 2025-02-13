"""
Import all the distances related classes from the Rust implementation.
"""
# pylint: disable=no-name-in-module
from xi_covutils.rs_covutils import distances_rs
js_distance = distances_rs.js_distance
kl_divergence = distances_rs.kl_divergence
