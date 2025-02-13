# Heterogeneity-Index

Python library to compute the Heterogeneity Index from SST, as defined in [Haëck et al. (2023)][haeck 2023] and [Liu & Levine (2016)][liu 2016].

Some filters are provided that can be applied to the input field before front detection.
Some diagnostics relying on fronts detection may be available in the future 🚧.

Documentation: https://biofronts.pages.in2p3.fr/heterogeneity-index

## Installation

From PyPI:
``` sh
pip install heterogeneity-index
```

From source:
``` sh
git clone https://gitlab.in2p3.fr/biofronts/heterogeneity-index
cd heterogeneity-index
pip install -e .
```

## Requirements

- Python >= 3.10
- Numpy >= 1.24
- Numba >= 0.57

Optional but recommended:
- Xarray
- Dask

## References
- Haëck, C., Lévy, M., Mangolte, I., and Bopp, L.: “Satellite data reveal earlier and stronger phytoplankton blooms over fronts in the Gulf Stream region”, *Biogeosciences* **20**, 1741–1758, https://doi.org/10.5194/bg-20-1741-2023, 2023.
- Liu, X. and Levine, N. M.: “Enhancement of phytoplankton chlorophyll by submesoscale frontal dynamics in the North Pacific Subtropical Gyre”, *Geophys. Res. Lett.* **43**, 1651–1659, https://doi.org/10.1002/2015gl066996, 2016.

[haeck 2023]: https://doi.org/10.5194/bg-20-1741-2023
[liu 2016]: https://doi.org/10.1002/2015gl066996
