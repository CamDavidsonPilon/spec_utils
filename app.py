import streamlit as st
import pandas as pd
import numpy as np
import os
from utils import *
from plotting import *


st.title('Excitation-Emission matrix analyzer')


def file_selector(folder_path='./sample_data'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


@st.cache
def load_data(filename):
    df = eem_dat_file_to_df(filename)
    return df


df = load_data(file_selector())


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.text('Excitation (rows) by Emissions (cols)')
    st.write(df)


st.header("Emission Spectra")
excitation_selection = st.slider('Excitation wavelength', df.index.min(), df.index.max(), step=1.0)
fig, ax = plt.subplots(figsize=(9, 7))
rayleigh_scattering_to_nan(df, 50).loc[excitation_selection].plot(ax=ax)
st.pyplot(fig)



st.header('Heatmap')

mask_ray = st.checkbox('Mask Rayleigh scatter?', value=True)
mask_raman = st.checkbox('Mask Raman scatter?')
log_scale = st.checkbox('Log scale?')
remove_upper_tri = st.checkbox('Remove upper triangle?')

st.pyplot(eem_heatmap(df,
    rayleigh_scattering_mask_width=25 if mask_ray else 0,
    raman_scattering_mask_width=10 if mask_raman else 0,
    log_scale=log_scale,
    plot_peaks=False,
    remove_upper_tri=remove_upper_tri,
    )[0])
