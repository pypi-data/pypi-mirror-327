"""Implementation of Belkin-O'Reilly Algorithm."""

from __future__ import annotations

from collections.abc import Callable, Collection, Hashable
from typing import TYPE_CHECKING

import numpy as np
from numba import guvectorize, jit, prange

from .util import is_dask_collection

if TYPE_CHECKING:
    import dask.array as da
    import xarray as xr

DEFAULT_DIMS: list[Hashable] = ["lat", "lon"]
"""Default dimensions names to use if none are provided.

...in the case of Xarray data and where the *dims* argument is None and *window_size*
is not a Mapping.
"""


# def boa(
#     input_field: xr.DataArray,
#     iterations: int = 1,
#     dims: Collection[Hashable] | None = None,
# ) -> xr.DataArray:
#     """Apply Belkin--O'Reilly Algorithm filter."""
#     pass


# def boa_dask(
#     input_field: da.Array, iterations: int = 1, axis: Collection[int] | None = None
# ) -> da.Array:
#     """Apply Belkin--O'Reilly Algorithm filter."""
#     pass


# def boa_numpy(
#     input_field: np.ndarray, iterations: int = 1, axis: Collection[int] | None = None
# ) -> np.ndarray:
#     pass


def contextual_median3(
    input_field: xr.DataArray,
    iterations: int = 1,
    dims: Collection[Hashable] | None = None,
) -> xr.DataArray:
    """Apply contextual median filter of size 3."""
    if dims is None:
        dims = DEFAULT_DIMS

    if len(dims) != 2:
        raise IndexError(f"`dims` should be of length 2 ({dims})")

    # We also find the dimensions indices to send to subfunctions
    axis = [input_field._get_axis_num(d) for d in dims]

    # I don't use xr.apply_ufunc because the dask function is quite complex
    # and cannot be dealt with only with dask.apply_gufunc (which is what
    # apply_ufunc does).

    func: Callable
    if is_dask_collection(input_field.data):
        func = contextual_median3_dask
    else:
        func = contextual_median3_numpy

    output = func(input_field.data, iterations=iterations, axis=axis)

    arr = xr.DataArray(
        data=output,
        coords=input_field.coords,
        dims=input_field.dims,
        name=f"{input_field.name}_CMF3",
        attrs=dict(computed_from=input_field.name, iterations=iterations),
    )
    return arr


def contextual_median3_dask(
    input_field: da.Array,
    iterations: int = 1,
    axis: Collection[int] | None = None,
) -> xr.DataArray:
    """Apply contextual median filter of size 3."""
    # Reorder axes if needed
    reorder = False
    if axis is not None:
        if len(axis) != 2:
            raise ValueError("`axis` argument must be of length 2")
        # make axis positive, as we add a new dimension later it
        # may not correspond to the user input anymore
        ndim = input_field.ndim
        axis = [i % ndim for i in axis]
        # sort the axis, we don't need to swap x/y
        axis.sort()
        # place those axis at the end for the gufunc
        if axis != [ndim - 2, ndim - 1]:
            reorder = True
            # note this is a view of the original array
            input_field = da.moveaxis(input_field, axis, [-2, -1])

    # Generate overlap if needed. ie if lon and/or lat dimensions are chunked, expand
    # each chunk with data from his neighbors to accomodate the sliding window.
    # The array outer edges are not expanded (boundary='none')
    depth = {ndim - 2: 1, ndim - 1: 1}
    overlap = da.overlap.overlap(input_field, depth=depth, boundary="none")

    # Do the computation for each chunk separately. All consideration of sharing
    # edges is dealt with by the overlap.
    output = da.map_blocks(
        _contextual_median3,
        overlap,
        new_axis=ndim,
        meta=np.array((), dtype=input_field.dtype),
    )

    # Trim back the expanded chunks
    output = da.overlap.trim_internal(output, depth)

    # Move back the axis to their original places
    if reorder:
        assert isinstance(axis, list)  # for mypy
        output = np.moveaxis(output, [-2, -1], axis)

    return output


def contextual_median3_numpy(
    input_field: np.ndarray,
    iterations: int = 1,
    axis: Collection[int] | None = None,
) -> np.ndarray:
    """Apply contextual median filter of size 3."""
    # Reorder axes if needed
    reorder = False
    if axis is not None:
        if len(axis) != 2:
            raise ValueError("`axis` argument must be of length 2")
        # make axis positive, as we add a new dimension later it
        # may not correspond to the user input anymore
        ndim = input_field.ndim
        axis = [i % ndim for i in axis]
        # sort the axis, we don't need to swap x/y
        axis.sort()
        # place those axis at the end for the gufunc
        if axis != [ndim - 2, ndim - 1]:
            reorder = True
            # note this is a view of the original array
            input_field = np.moveaxis(input_field, axis, [-2, -1])

    output = np.empty_like(input_field)
    for _ in range(iterations):
        _contextual_median3(input_field, output)

    # Move back the axis to their original places
    if reorder:
        assert isinstance(axis, list)  # for mypy
        output = np.moveaxis(output, [-3, -2], axis)

    return output


@jit(nopython=True, cache=True, nogil=True)
def is_max_at(arr: np.ndarray, at: int) -> bool:
    flat = arr.flatten()
    max_idx = np.argmax(flat)
    if max_idx != at:
        return False

    # check if multiple counts of value
    max_val = flat[max_idx]
    if np.any(np.isclose(max_val, flat[max_idx + 1 :])):
        return False

    return True


@jit(nopython=True, cache=True, nogil=True)
def is_min_at(arr: np.ndarray, at: int) -> bool:
    flat = arr.flatten()
    min_idx = np.argmin(flat)
    if min_idx != at:
        return False

    # check if multiple counts of value
    min_val = flat[min_idx]
    if np.any(np.isclose(min_val, flat[min_idx + 1 :])):
        return False

    return True


@jit(nopython=True, cache=True, nogil=True, debug=True)
def _is_peak5(window: np.ndarray) -> bool:
    is_peak = (
        is_max_at(window[2, :], 2)  # accross
        and is_max_at(window[:, 2], 2)  # down
        and is_max_at(np.diag(window), 2)  # down diagonal
        and is_max_at(np.diag(window.T), 2)  # up diagonal
    ) or (
        is_min_at(window[2, :], 2)  # accross
        and is_min_at(window[:, 2], 2)  # down
        and is_min_at(np.diag(window), 2)  # down diagonal
        and is_min_at(np.diag(window.T), 2)  # up diagonal
    )
    return is_peak


@jit(nopython=True, cache=True, nogil=True)
def _apply_cmf3_filter(window, center_x, center_y, output):
    """Apply contextual median filter."""
    peak3 = is_max_at(window, 4) or is_min_at(window, 4)
    if peak3:
        output[center_y, center_x] = np.median(window)


@guvectorize(
    [
        "(float32[:, :], float32[:, :])",
        "(float64[:, :], float64[:, :])",
    ],
    "(y,x)->(y,x)",
    nopython=True,
    target="parallel",
    cache=True,
)
def _boa(field, output):
    output[:] = field.copy()
    ny, nx = field.shape

    # Start with the center (where we have a 5-window)
    for center_y in prange(2, ny - 2):
        slice_5y = slice(center_y - 2, center_y + 3)
        slice_3y = slice(center_y - 1, center_y + 2)
        for center_x in prange(2, nx - 2):
            slice_5x = slice(center_x - 2, center_x + 3)

            if _is_peak5(field[slice_5y, slice_5x]):
                continue

            slice_3x = slice(center_x - 1, center_x + 2)
            window = field[slice_3y, slice_3x]
            _apply_cmf3_filter(window, center_x, center_y, output)

    # Sides: peak5 is False there (by default)
    for center_x in prange(1, nx - 1):
        slice_x = slice(center_x - 1, center_x + 2)
        # top
        window = field[:3, slice_x]
        _apply_cmf3_filter(window, center_x, 1, output)
        # bottom
        window = field[ny - 3 :, slice_x]
        _apply_cmf3_filter(window, center_x, ny - 1, output)

    for center_y in prange(1, ny - 1):
        slice_y = slice(center_y - 1, center_y + 2)
        # left
        window = field[slice_y, :3]
        _apply_cmf3_filter(window, 1, ny - 1, output)
        # right
        window = field[slice_y, nx - 3 :]
        _apply_cmf3_filter(window, nx - 1, center_y, output)


@guvectorize(
    [
        "(float32[:, :], float32[:, :])",
        "(float64[:, :], float64[:, :])",
    ],
    "(y,x)->(y,x)",
    nopython=True,
    target="parallel",
    cache=True,
)
def _contextual_median3(field, output):
    output[:] = field.copy()
    ny, nx = field.shape

    for center_y in prange(1, ny - 1):
        slice_y = slice(center_y - 1, center_y + 2)
        for center_x in prange(1, nx - 1):
            slice_x = slice(center_x - 1, center_x + 2)
            window = field[slice_y, slice_x].flatten()
            _apply_cmf3_filter(window, center_x, center_y, output)
