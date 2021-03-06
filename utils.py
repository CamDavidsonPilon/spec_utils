# utils.py

import pandas as pd
import numpy as np


def eem_dat_file_to_df(filename, verbose=True):
    if verbose:
        print("### Opening file %s" % filename)
    df = pd.read_csv(
        filename,
        header=0,
        skiprows=[1, 2],
        index_col=0,
        delimiter=r"\s",
        engine="python",
    )


    df.columns = [np.round(float(s), 1) for s in df.columns]
    df.index = [np.round(s, 1) for s in df.index]
    df.index.name = "Emission (nm)"
    df.columns.name = "Excitation (nm)"
    df.filename = filename

    df = df.sort_index(axis=1, ascending=False)
    df = df.sort_index(axis=0, ascending=True)
    df = df.dropna()
    df = df.T

    return df


def rayleigh_scattering_mask(df, mask_width=10):

    emissions = df.columns.values
    excitations = df.index.values

    mask = np.abs(np.subtract.outer(excitations, emissions)) < mask_width
    return mask


def rayleigh_scattering_to_nan(df, mask_width=10):
    df = df.copy()
    mask = rayleigh_scattering_mask(df, mask_width=mask_width)
    df.values[mask] = np.nan
    return df

def block_mask(df, position, fraction):

    r, c = df.shape
    mask = np.zeros_like(df, dtype=bool)

    if position == "left":
        mask[:, int(c * fraction) :] = True
    elif position == "right":
        mask[:, int((1 - c) * fraction) :] = True
    elif position == "top":
        mask[: int((1 - c) * fraction), :] = True
    elif position == "bottom":
        mask[int(c * fraction) :, :] = True
    else:
        raise ValueError("position must be 'left', 'right', 'top', 'bottom'")
    return mask


def upper_tri_mask(df):

    emissions = df.columns.values
    excitations = df.index.values

    mask = np.greater.outer(excitations, emissions)
    return mask


def water_raman_scattering_mask(df, mask_width=5):

    WATER_RAMAN_SHIFT = np.exp(-(np.log(3400) + np.log(3600)) / 2)
    emissions = df.columns.values
    excitations = df.index.values
    sorter = np.argsort(emissions)

    mask = np.zeros_like(df, dtype=bool)

    for ix, ex in enumerate(excitations):
        raman_wl = 1 / (1 / ex - WATER_RAMAN_SHIFT)
        iy = np.searchsorted(emissions, raman_wl, sorter=sorter)

        try:
            mask[ix, iy - mask_width : iy + mask_width] = True
        except:
            continue

    return mask
