"""Fill single invalid pixels."""

from __future__ import annotations

from collections.abc import Collection, Hashable, Sequence
from typing import TYPE_CHECKING, TypeVar

import numpy as np
from numba import guvectorize, prange

from ..util import FuncMapper

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from ..util import DaskArray, XarrayArray

DEFAULT_DIMS: list[Hashable] = ["lat", "lon"]
"""Default dimensions names."""


def fill_numpy(
    input_field: NDArray, axes: Sequence[int] | None = None, **kwargs
) -> NDArray:
    """Filter that fill single invalid pixels.

    A single invalid pixel being one pixel surrounded by 8 valid pixel in the 3x3 square
    window around it.

    Parameters
    ----------
    input_field:
        Input array to filter.
    axes:
        Indices of the the y/lat and x/lon axes on which to work. If None (default), the
        last two axes are used.
    kwargs:
        See available kwargs for universal functions at
        :external+numpy:ref:`c-api.generalized-ufuncs`.

    Returns
    -------
    filled_field:
        Filled array.
    """
    if axes is not None:
        # (y,x),(y,x)->(y,x)
        kwargs["axes"] = [tuple(axes), tuple(axes)]

    output = _fill(input_field, **kwargs)
    return output


def fill_dask(
    input_field: DaskArray, axes: Sequence[int] | None = None, **kwargs
) -> DaskArray:
    """Filter that fill single invalid pixels.

    A single invalid pixel being one pixel surrounded by 8 valid pixel in the 3x3 square
    window around it.

    Parameters
    ----------
    input_field:
        Input array to filter.
    axes:
        Indices of the the y/lat and x/lon axes on which to work. If None (default), the
        last two axes are used.
    kwargs:
        See available kwargs for universal functions at
        :external+numpy:ref:`c-api.generalized-ufuncs`.

    Returns
    -------
    filled_field:
        Filled array.
    """
    import dask.array as da

    if axes is not None:
        # (y,x)->(y,x)
        kwargs["axes"] = [tuple(axes), tuple(axes)]

    ndim = input_field.ndim
    output = da.map_overlap(
        _fill, input_field, depth={ndim - 2: 1, ndim - 1: 1}, **kwargs
    )
    return output


fill_mapper = FuncMapper("fill", numpy=fill_numpy, dask=fill_dask)


def fill_xarray(
    input_field: XarrayArray, dims: Collection[Hashable] | None = None, **kwargs
) -> XarrayArray:
    """Filter that fill single invalid pixels.

    A single invalid pixel being one pixel surrounded by 8 valid pixel in the 3x3 square
    window around it.

    Parameters
    ----------
    input_field:
        The field to apply the filter to.
    dims:
        Names of the dimensions along which to compute the index. Order is irrelevant,
        no reordering will be made between the two dimensions.
        If the `window_size` argument is given as a mapping, its keys are used instead.
        If not specified, is taken by module-wide variable :data:`DEFAULT_DIMS`
        which defaults to ``{'lat', 'lon'}``.
    kwargs:
        See available kwargs for universal functions at
        :external+numpy:ref:`c-api.generalized-ufuncs`.

    Returns
    -------
    filled_field:
        Filled array.
    """
    import xarray as xr

    if dims is None:
        dims = DEFAULT_DIMS
    # make sure we have a copy
    dims = list(dims)

    if len(dims) != 2:
        raise IndexError(f"`dims` should be of length 2 ({dims})")

    axes = sorted([input_field._get_axis_num(d) for d in dims])

    func = fill_mapper.get_func(input_field.data)
    output = func(input_field.data, axes=axes)

    # Output dataset
    da = xr.DataArray(
        output,
        coords=input_field.coords,
        dims=input_field.dims,
        name=input_field.name,
    )
    return da


_DT = TypeVar("_DT", bound=np.dtype[np.float32] | np.dtype[np.float64])


@guvectorize(
    ["(float32[:, :], float32[:, :])", "(float64[:, :], float64[:, :])"],
    "(y,x)->(y,x)",
    nopython=True,
    target="parallel",
    cache=True,
)
def _fill(
    field: np.ndarray[tuple[int, ...], _DT], output: np.ndarray[tuple[int, ...], _DT]
):
    """Apply fill filter to array.

    .. warning:: Internal function.

        Users should rather use :func:`fill_numpy`.

    *Numba options:*
        ``nopython=True``, ``cache=True``, ``target="parallel"``

    *Signatures:*
        - (float32[:, :], float32[:, :])
        - (float64[:, :], float64[:, :])

    Note this filter could be done in-place, but this is incompatible with dask arrays.
    """
    ny, nx = field.shape
    output[:] = field
    mask = ~np.isfinite(field)

    # window where a fill is needed (only central pixel is invalid)
    isinvalid_to_fill = np.array(
        ((False, False, False), (False, True, False), (False, False, False))
    )

    for center_y in prange(1, ny - 1):
        slice_y = slice(center_y - 1, center_y + 2)
        for center_x in prange(1, nx - 1):
            slice_x = slice(center_x - 1, center_x + 2)
            if np.all(mask[slice_y, slice_x] == isinvalid_to_fill):
                window = field[slice_y, slice_x]
                output[center_y, center_x] = np.nanmedian(window)
