# plotting
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.feature import peak_local_max
import numpy as np
from utils import rayleigh_scattering_mask, upper_tri_mask, water_raman_scattering_mask

sns.set()


def eem_heatmap(
    df,
    rayleigh_scattering_mask_width=0,
    raman_scattering_mask_width=0,
    remove_upper_tri=False,
    additional_mask=None,
    plot_peaks=False,
    log_scale=False,
    title=None,
    normalize=True,
):
    """
    df: DataFrame
        should be a DataFrame from eem_dat_file_to_df, with excitation as columns and emission as index
    rayleigh_scattering_mask_width: int
        width of mask of the scattering along the y=x line.
    raman_scattering_mask_width: int
        width of mask of the scattering along the water-raman scattering line.
    additional_mask: numpy array
        a numpy array of the same size as df with boolean values. True values will not be displayed.
    remove_upper_tri: bool
        remove the values where excitation < emission
    log_scale: bool
        apply a log-transform.
    normalize: bool
        map the values between 0 and 1.

    """
    df = df.copy()

    mask = np.zeros_like(df, dtype=bool)

    mask |= rayleigh_scattering_mask(df, rayleigh_scattering_mask_width)

    if raman_scattering_mask_width > 0:
        mask |= water_raman_scattering_mask(df, raman_scattering_mask_width)

    if remove_upper_tri:
        mask |= upper_tri_mask(df)

    if additional_mask is not None:
        mask |= additional_mask

    if normalize:
        df = (df - df.values[~mask].min())
        df = df / df.values[~mask].max()

    if log_scale:
        df = np.log(df - df.values[~mask].min() + 1)

    fig, ax = plt.subplots(figsize=(7, 6))


    ax = sns.heatmap(df, ax=ax,
        mask=mask,
        vmax=df.values[~mask].max(),
        vmin=df.values[~mask].min(),
        cmap="viridis",
        cbar_kws={'label': "Arbitrary Intensity (A.U.), normalized" if normalize else "Arbitrary Intensity (A.U.)"})
    ax.set_title(title, fontsize=16)

    xt, xtl = ax.get_xticks(), ax.get_xticklabels()
    ax.set_xticks(xt[::2])
    ax.set_xticklabels(xtl[::2])

    yt, ytl = ax.get_yticks(), ax.get_yticklabels()
    ax.set_yticks(yt[::2])
    ax.set_yticklabels(ytl[::2])


    ax.xaxis.label.set_size(13)
    ax.yaxis.label.set_size(13)


    if plot_peaks:
        coor = peak_local_max(
            df.values, min_distance=20, exclude_border=True, threshold_rel=0.01
        )
        for x, y in coor:
            if not mask[x, y]:
                ax.scatter(y, x, c="b", s=15, edgecolors="k", linewidths=0.5)


    plt.tight_layout()
    return fig, ax
