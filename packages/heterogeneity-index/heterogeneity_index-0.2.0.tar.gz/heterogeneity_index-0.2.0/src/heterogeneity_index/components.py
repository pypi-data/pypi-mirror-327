"""Functions for computing the components of the HI.

This modules provides three public functions depending on the type of the input
field:

- :func:`compute_components_numpy` for Numpy arrays.
- :func:`compute_components_dask` for Dask arrays. It can handle arrays chunked
  along any dimensions.
- :func:`compute_components_xarray` for Xarray DataArrays (this function defers
  work to one of the two other functions, depending on the inner datatype).

.. rubric:: Window size and reach

Users input the moving window size as the total length in number of pixels. It is
however useful to work with the number of pixels between the center and the edge.
We call this value the window "reach". It counts the number of pixels beween the center
(excluding it) and the border pixel (including it).
For a window of size 3 will have a reach of 1, a window of size 7 a reach of size 3.
"""

# This file is part of the 'heterogeneity-index' project
# (https://gitlab.in2p3.fr/biofronts/heterogeneity-index)
# and subject to the MIT License as defined in the file 'LICENSE',
# at the root of this project.
# © 2023 Clément Haëck, CNRS

from __future__ import annotations

import logging
from collections.abc import Collection, Hashable, Mapping, Sequence
from typing import TYPE_CHECKING, Any, TypeVar

import numpy as np
from numba import guvectorize, jit, prange

from .util import FuncMapper

if TYPE_CHECKING:
    from numpy.typing import NDArray

    # deals with conditionnal import
    from .util import DaskArray, XarrayArray, XarrayDataset


logger = logging.getLogger(__name__)

COMPONENTS_NAMES = ["stdev", "skew", "bimod"]
"""Components short name, in their order of appearance in function signatures."""

DEFAULT_DIMS: list[Hashable] = ["lat", "lon"]
"""Default dimensions names.

Used for Xarray input where the *dims* argument is None and *window_size*
is not a Mapping.
"""


def compute_components_numpy(
    input_field: NDArray,
    window_size: int | Sequence[int],
    bins_width: float = 0.1,
    bins_shift: float = 0.0,
    axes: Sequence[int] | None = None,
    **kwargs,
) -> tuple[NDArray, NDArray, NDArray]:
    """Compute components from a Numpy array.

    Parameters
    ----------
    input_field:
        Array of the input field from which to compute the heterogeneity index.
    window_size:
        Total size of the moving window, in pixels. If an integer, the size is taken
        identical for both axis. Otherwise it must be a sequence of 2 integers
        specifying the window size along both axis. The order must then follow that of
        the data. For instance, for data arranged as ('time', 'lat', 'lon') if we
        specify ``window_size=[3, 5]`` the window will be of size 3 along latitude and
        size 5 for longitude.
    bins_width:
        Width of the bins used to construct the histogram when computing the
        bimodality.
    bins_shift:
        If non-zero, shift the leftmost and rightmost edges of the bins by
        this amount to avoid artefacts caused by the discretization of the
        input field data.
    axes:
        Indices of the the y/lat and x/lon axes on which to work. If None (default), the
        last two axes are used.
    kwargs:
        See available kwargs for universal functions at
        :external+numpy:ref:`c-api.generalized-ufuncs`.

    Returns
    -------
    components:
        Tuple of components, in the order of :attr:`COMPONENTS_NAMES`.
    """
    window_reach = get_window_reach(window_size)

    if bins_width == 0.0:
        raise ValueError("bins_width cannot be 0.")

    if axes is not None:
        # (y,x),(c),(w),(),()->(y,x,c)
        kwargs["axes"] = [tuple(axes), (0), (0), (), (), (*axes, input_field.ndim)]

    output = _compute_components(
        input_field,
        list(range(3)),  # dummy argument of size 3, needed to accomadate dask
        window_reach,
        bins_width,
        bins_shift,
        **kwargs,
    )

    stdev = output[..., 0]
    skew = output[..., 1]
    bimod = output[..., 2]

    return stdev, skew, bimod


def compute_components_dask(
    input_field: DaskArray,
    window_size: int | Sequence[int],
    bins_width: float = 0.1,
    bins_shift: float = 0.0,
    axes: Sequence[int] | None = None,
    **kwargs,
) -> tuple[DaskArray, DaskArray, DaskArray]:
    """Compute components from Dask array.

    Parameters
    ----------
    input_field:
        Array of the input field from which to compute the heterogeneity index.
    window_size:
        Total size of the moving window, in pixels. If an integer, the size is taken
        identical for both axis. Otherwise it must be a sequence of 2 integers
        specifying the window size along both axis. The order must then follow that of
        the data. For instance, for data arranged as ('time', 'lat', 'lon') if we
        specify ``window_size=[3, 5]`` the window will be of size 3 along latitude and
        size 5 for longitude.
    bins_width:
        Width of the bins used to construct the histogram when computing the
        bimodality.
    bins_shift:
        If non-zero, shift the leftmost and rightmost edges of the bins by
        this amount to avoid artefacts caused by the discretization of the
        input field data.
    axes:
        Indices of the the y/lat and x/lon axes on which to work. If None (default), the
        last two axes are used.
    kwargs:
        See available kwargs for universal functions at
        :external+numpy:ref:`c-api.generalized-ufuncs`.

    Returns
    -------
    components:
        Tuple of components, in the order of :attr:`COMPONENTS_NAMES`.

    Raises
    ------
    ValueError: ``bins_width`` cannot be 0.
    TypeError: ``axis`` must be of length 2.
    """
    import dask.array as da

    window_reach_x, window_reach_y = get_window_reach(window_size)

    if bins_width == 0.0:
        raise ValueError("bins_width cannot be 0.")

    # Generate overlap if needed. ie if lon and/or lat dimensions are chunked, expand
    # each chunk with data from his neighbors to accomodate the sliding window.
    # The array outer edges are not expanded (boundary='none')
    ndim = input_field.ndim
    depth = {ndim - 2: window_reach_y, ndim - 1: window_reach_x}
    overlap = da.overlap.overlap(input_field, depth=depth, boundary="none")

    if axes is not None:
        # (y,x),(c),(w),(),()->(y,x,c)
        kwargs["axes"] = [tuple(axes), (0), (0), (), (), (*axes, input_field.ndim)]

    # Do the computation for each chunk separately. All consideration of sharing
    # edges is dealt with by the overlap.
    output = da.map_blocks(
        _compute_components,  # compiled function
        # arguments to the function
        overlap,
        list(range(3)),  # dummy argument of size 3
        (window_reach_x, window_reach_y),
        bins_width,
        bins_shift,
        **kwargs,
        # metadata to deal with additional axis for components, and also I don't
        # trust automatic inference
        new_axis=ndim,
        meta=np.array((), dtype=input_field.dtype),
        chunks=tuple([*overlap.chunks, 3]),
    )

    # Trim back the expanded chunks
    output = da.overlap.trim_internal(output, depth)

    stdev = output[..., 0]
    skew = output[..., 1]
    bimod = output[..., 2]

    return stdev, skew, bimod


def compute_components_xarray(
    input_field: XarrayArray,
    window_size: int | Mapping[Hashable, int] | Sequence[int],
    bins_width: float = 0.1,
    bins_shift: float | bool = True,
    dims: Collection[Hashable] | None = None,
) -> XarrayDataset:
    """Compute components from Xarray data.

    Parameters
    ----------
    input_field:
        Array of the input field from which to compute the heterogeneity index.
    window_size:
        Total size of the moving window, in pixels. If a single integer, the size is
        taken identical for both axis. Otherwise it can be a mapping of the dimensions
        names to the window size along this axis.
        It can also be a sequence of 2 integers specifying the window size along both
        axis. The order must then follow that of the data. For instance, for data
        arranged as ('time', 'lat', 'lon') if we specify ``window_size=[3, 5]`` the
        window will be of size 3 along latitude and size 5 for longitude.
    bins_width:
        Width of the bins used to construct the histogram when computing the
        bimodality.
    bins_shift:
        If a non-zero :class:`float`, shift the leftmost and rightmost edges of
        the bins by this amount to avoid artefacts caused by the discretization
        of the input field data.
        If `True` (default), wether to shift and by which amount is determined using
        the input metadata.

        Set to 0 or `False` to not shift bins.
    dims:
        Names of the dimensions along which to compute the index. Order is irrelevant,
        no reordering will be made between the two dimensions.
        If the `window_size` argument is given as a mapping, its keys are used instead.
        If not specified, is taken by module-wide variable :data:`DEFAULT_DIMS`
        which defaults to ``{'lat', 'lon'}``.

    Returns
    -------
    Dataset containing the components as three variables.
    """
    if bins_width == 0.0:
        raise ValueError("bins_width cannot be 0.")

    # Detect if we should shift bins
    if bins_shift is True:
        scale_factor = input_field.encoding.get("scale_factor", None)
        if scale_factor is None:
            logger.warning(
                "Did not find `scale_factor` in the encoding of variable '%s'. "
                "Bins will not be shifted. Set the value of the `bins_shift` argument "
                "manually, or set it to False to silence this warning.",
                input_field.name,
            )
            bins_shift = 0.0
        else:
            bins_shift = scale_factor / 2
            logger.debug("Shifting bins by %g.", bins_shift)
    else:
        bins_shift = 0.0

    if dims is None:
        if isinstance(window_size, Mapping):
            dims = list(window_size.keys())
        else:
            dims = DEFAULT_DIMS

    # make sure we have a copy
    dims = list(dims)

    if isinstance(window_size, int):
        window_size = {d: window_size for d in dims}
    elif not isinstance(window_size, Mapping):
        if len(window_size) != 2:
            raise IndexError(
                "Window size given as a sequence must be of length 2 "
                f"(received {window_size})"
            )
        window_size = {d: size for d, size in zip(dims, window_size, strict=True)}

    return _compute_components_xarray_inner(
        input_field, window_size, bins_width, bins_shift, dims
    )


components_mapper = FuncMapper(
    "components",
    numpy=compute_components_numpy,
    dask=compute_components_dask,
)


def _compute_components_xarray_inner(
    input_field: XarrayArray,
    window_size: Mapping[Hashable, int],
    bins_width: float,
    bins_shift: float,
    dims: Collection[Hashable],
) -> XarrayDataset:
    import xarray as xr

    if len(dims) != 2:
        raise IndexError(f"`dims` should be of length 2 ({dims})")
    if len(window_size) != 2:
        raise IndexError(f"`window_size` should be of length 2 ({window_size})")
    if set(window_size.keys()) != set(dims):
        raise ValueError(
            f"Dimensions from `dims` ({dims}) and "
            f"`window_size` ({window_size}) are incompatible."
        )

    # Order the window_size like the data
    window_size_seq = [window_size[d] for d in input_field.dims if d in dims]

    # We also find the dimensions indices to send to subfunctions
    axes = sorted([input_field._get_axis_num(d) for d in dims])

    # I don't use xr.apply_ufunc because the dask function is quite complex
    # and cannot be dealt with only with dask.apply_gufunc (which is what
    # apply_ufunc does).

    func = components_mapper.get_func(input_field.data)
    # output is a tuple of array (either numpy or dask)
    output = func(
        input_field.data,
        window_size=window_size_seq,
        bins_width=bins_width,
        bins_shift=bins_shift,
        axes=axes,
    )

    # Attribute common to all variable (and also global attributes)
    common_attrs: dict = {f"window_size_{d}": window_size[d] for d in dims}
    common_attrs["window_size"] = tuple(window_size.values())
    from_name = input_field.attrs.get("standard_name", input_field.name)
    if from_name is not None:
        common_attrs["computed_from"] = from_name

    components_attrs: dict[str, Any] = {
        "stdev": dict(long_name="Standard deviation component not normalized"),
        "skew": dict(long_name="Skewness component not normalized"),
        "bimod": dict(long_name="Bimodality component not normalized"),
    }
    for c, attrs in components_attrs.items():
        attrs["standard_name"] = c
        attrs.update(common_attrs)

    # Output dataset
    ds = xr.Dataset(
        {
            name: (input_field.dims, arr, components_attrs[name])
            for name, arr in zip(COMPONENTS_NAMES, output, strict=True)
        },
        coords=input_field.coords,
        attrs=common_attrs,
    )

    return ds


def get_window_reach(window_size: int | Sequence[int]) -> list[int]:
    """Return window reach as a tuple."""
    if isinstance(window_size, int):
        window_size = [window_size] * 2

    if any(w % 2 != 1 for w in window_size):
        raise ValueError(f"Window size must be odd (received {window_size})")

    window_reach = list(int(np.floor(w / 2)) for w in window_size)
    return window_reach


@jit(
    [
        "float32[:](float32[:], float64, float64)",
        "float64[:](float64[:], float64, float64)",
    ],
    nopython=True,
    cache=True,
    nogil=True,
)
def _get_components_from_values(
    values: NDArray,
    bins_width: float,
    bins_shift: float,
) -> NDArray:
    """Compute components from sequence of values (in the sliding window).

    This function is compiled just-in-time using :func:`numba.jit`.

    *Numba options:*
        ``nopython=True``, ``cache=True``, ``nogil=True``.

    Parameters
    ----------
    values:
        Array of values from the sliding window. Should only contain valid
        (finite) values.
    bins_width:
        Width of the bins used to construct the histogram when computing the
        bimodality. Must have same units and same data type as the input array.
    bins_shift:
        If non-zero, shift the leftmost and rightmost edges of the bins by
        this amount to avoid artefacts caused by the discretization of the
        input field data.
    kwargs:
        See available kwargs for universal functions at
        :external+numpy:ref:`c-api.generalized-ufuncs`.

    Returns
    -------
    components:
        Tuple of the three components (scalar values): standard deviation,
        skewness, and bimodality. In this order.
    """
    avg = np.mean(values)
    n_values = values.size

    # First component: standard deviation
    stdev = np.sqrt(np.sum((values - avg) ** 2) / (n_values - 1))

    # avoid invalid computations if there is no variation in values
    if stdev < 1e-6:
        return np.asarray([stdev, 0.0, 0.0], dtype=values.dtype)

    # Second component: skewness
    skewness = np.sum((values - avg) ** 3) / n_values / stdev**3

    # Third component: bimodality
    v_min = np.min(values)
    v_max = np.max(values)

    # mininum number of bins necessary for computation
    n_min_bin = 4

    # Shift the bins if necessary
    if bins_shift != 0.0:
        v_min -= bins_shift
        v_max += bins_shift

    n_bins = int(np.floor((v_max - v_min) / bins_width) + 1)
    if n_bins <= n_min_bin:
        bimod = 0.0
    else:
        # numba implements a fast histogram method, not normalised
        hist, bins = np.histogram(values, bins=n_bins, range=(v_min, v_max))

        # -> to get a probability density function:
        # widths = np.diff(bins)
        # freq = hist / widths
        # we then normalise to have an integral equal to 1
        # pdf = freq / np.sum(freq * widths)
        # which is equivalent to:
        pdf = hist / np.diff(bins) / np.sum(hist)

        # create the gaussian to compare the histogram to
        gauss = np.exp(-0.5 * ((bins - avg) / stdev) ** 2) / (
            stdev * np.sqrt(2 * np.pi)
        )

        # We compare the histogram to the integral of the gaussian,
        # using the trapezoidal rule
        bimod = np.sum(np.abs(pdf - 0.5 * (gauss[:n_bins] + gauss[1:]))) * bins_width

    return np.asarray([stdev, skewness, bimod], dtype=values.dtype)


_DT = TypeVar("_DT", bound=np.dtype[np.float32] | np.dtype[np.float64])


@guvectorize(
    [
        "(float32[:, :], intp[:], intp[:], float64, float64, float32[:, :, :])",
        "(float64[:, :], intp[:], intp[:], float64, float64, float64[:, :, :])",
    ],
    "(y,x),(c),(w),(),()->(y,x,c)",
    nopython=True,
    target="parallel",
    cache=True,
)
def _compute_components(
    input_image: np.ndarray[tuple[int, ...], _DT],
    dummy: tuple[int, int, int],
    window_reach: np.ndarray[tuple[int], np.dtype[np.integer]],
    bins_width: float,
    bins_shift: float,
    output: np.ndarray[tuple[int, ...], _DT],
):
    """_compute_components(input_image, dummy, window_reach, bins_width, bins_shift, out=None)
    Compute HI components from input field image.

    .. warning:: Internal function.

        Users should rather use :func:`compute_components_numpy`.

    This function is compiled and transformed into a Numpy generalized
    universal function (see
    :external+numpy:doc:`reference/c-api/generalized-ufuncs`), using the
    :func:`numba.guvectorize` decorator. This means that any additional
    dimensions in the input array will automatically be looped over.

    *Numba options:*
        ``nopython=True``, ``target='parallel'``, ``cache=True``.

    *Signatures:*
        - (float32[:, :], intp[:], intp[:], float64, float64, float32[:, :, :])
        - (float64[:, :], intp[:], intp[:], float64, float64, float64[:, :, :])

    This function does not compute the components along the edges of the
    input image.

    Parameters
    ----------
    input_image:
        Array of the input field from which to compute the HI components.
        The last two dimensions of the array should correspond to the y and x
        axis of the input field image (the order does not matter).
        Invalid values must be marked as `np.nan` (this is the behavior of
        Xarray: see :external+xarray:ref:`missing_values`).
    dummy:
        Dummy argument that must be of size 3 (corresponding to the number of
        components).
        We need to have a single output array for when using Dask (thus with an
        additional dimension for the 3 components), but
        :func:`numba.guvectorize` needs all the dimensions to be defined in the
        input variables. Details in :ref:`/implementation_details.rst`.
    window_reach:
        Reach of the window for each axis (y, x).
        The 'reach' is the number of pixels between the center pixel and the
        edge. For instance, a ``3x3`` window will have a reach of 1.

        The axis ordering **must** correspond to that of `input_image`. For instance, if
        `input_image` is ordered as ``[..., y, x]``, then `window_reach` must be ordered
        as ``[reach_y, reach_x]``.
    bins_width:
        Width of the bins used to construct the histogram when computing the
        bimodality. Must have same units and same data type as the input array.
    bins_shift:
        If non-zero, shift the leftmost and rightmost edges of the bins by
        this amount to avoid artefacts caused by the discretization of the
        input field data.

    Returns
    -------
    components: NDArray
        An array of the same size and datatype as the input one, with an
        additional dimension at the end to separate the 3 components. The
        components are in the following order: standard deviation, skewness,
        and bimodality.

    References
    ----------
    - Numpy GUFuncs: https://numpy.org/doc/stable/reference/c-api/generalized-ufuncs.html
    - Numba.guvectorize (guide): https://numba.pydata.org/numba-doc/dev/user/vectorize.html#the-guvectorize-decorator
    - Numba.guvectorize (API): https://numba.pydata.org/numba-doc/dev/reference/jit-compilation.html#numba.guvectorize
    """  # noqa: E501, D205
    window_reach_y, window_reach_x = window_reach
    img_size_y, img_size_x = input_image.shape

    # max number of pixel inside the moving window
    win_npixels = np.prod(2 * window_reach + 1)

    output[:] = np.nan

    mask = np.isfinite(input_image)

    # iterate over target pixels
    # we do not take the edges
    for target_y in prange(window_reach_y, img_size_y - window_reach_y):
        slice_y = slice(target_y - window_reach_y, target_y + window_reach_y + 1)
        for target_x in prange(window_reach_x, img_size_x - window_reach_x):
            slice_x = slice(target_x - window_reach_x, target_x + window_reach_x + 1)

            # select values in the moving window
            win_values = input_image[slice_y, slice_x].flatten()
            win_mask = mask[slice_y, slice_x].flatten()
            win_values_filtered = win_values[win_mask]

            # we only work if the number of valid values in the window
            # is above a threshold (half here)
            n_values = win_values_filtered.size
            if (n_values / win_npixels) < 0.5:
                continue

            # pass the array of values (we use ravel to make sure it is
            # contiguous in memory)
            output[target_y, target_x, :] = _get_components_from_values(
                np.ravel(win_values_filtered), bins_width, bins_shift
            )
