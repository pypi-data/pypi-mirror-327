"""Heterogeneity Index computation."""

from . import filters
from .components import (
    compute_components_dask,
    compute_components_numpy,
    compute_components_xarray,
)
from .normalization import (
    apply_coefficients,
    compute_coefficient_hi,
    compute_coefficients_components,
)

__version__ = "0.2.0"


__all__ = [
    "filters",
    "compute_components_dask",
    "compute_components_numpy",
    "compute_components_xarray",
    "apply_coefficients",
    "compute_coefficient_hi",
    "compute_coefficients_components",
]
