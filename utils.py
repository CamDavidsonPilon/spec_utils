# utils.py

import pandas as pd
import numpy as np

def eem_dat_file_to_df(filename, verbose=True):
    if verbose:
        print("   Opening file %s" % filename)
    df = pd.read_csv(filename,
        header=0,
        skiprows=[1,2],
        index_col=0,
        delimiter=r"\s",
        engine="python"
    )

    df.columns = [np.round(float(s), 1) for s in df.columns]
    df.index = [np.round(s, 1) for s in df.index]
    df.index.name = 'Emission'
    df.columns.name = 'Excitation'

    df = df.sort_index(axis=1, ascending=False)
    df = df.sort_index(axis=0, ascending=True)

    return df.T



def rayleigh_scattering_mask(df, mask_width=10):

    emissions = df.index.values
    excitations = df.columns.values

    mask = np.abs(np.subtract.outer(emissions, excitations)) < mask_width
    return mask


def block_mask(df, position, fraction):

    r, c = df.shape
    mask = np.zeros_like(df, dtype=bool)

    if position == "left":
        mask[:, int(c * fraction):] = True
    elif position == "right":
        mask[:, int((1-c) * fraction):] = True
    elif position == "top":
        mask[:int((1-c) * fraction), :] = True
    elif position == "bottom":
        mask[int(c * fraction):, :] = True
    else:
        raise ValueError("position must be 'left', 'right', 'top', 'bottom'")
    return mask


def upper_tri_mask(df):

    emissions = df.index.values
    excitations = df.columns.values

    mask = np.greater.outer(emissions, excitations)
    return mask
