import streamlit as st
import pandas as pd
import numpy as np
import os
from utils import *
from plotting import *
from path import PATH
from pathlib import Path


st.title('Excitation-Emission matrix analyzer')


def file_selector(folder_path=PATH):
    filenames = [file for file in os.listdir(folder_path) if file.endswith('.dat')]
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


@st.cache
def load_data(filename):
    df = eem_dat_file_to_df(filename)
    return df

choosen_file = file_selector()
df = load_data(choosen_file)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.text('Excitation (rows) by Emissions (cols)')
    st.write(df)


st.header("Emission Spectra")
excitation_selection = st.slider('Excitation wavelength', df.index.min(), df.index.max(), step=(df.index.max() - df.index.min())/(df.shape[0]-1))
# TODO: move into plotting module. Better: turn into an interactive plot.
slice_ = rayleigh_scattering_to_nan(df, 20).loc[excitation_selection]
st.line_chart(slice_)



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
    title=Path(choosen_file).name
    )[0], dpi=200)
