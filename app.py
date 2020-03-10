import streamlit as st
import pandas as pd
import numpy as np
import os
from utils import *
from plotting import *
from path import PATH
from pathlib import Path

@st.cache
def load_data(filename):
    df = eem_dat_file_to_df(filename)
    return df

#######################################################
#### Sidebar - file selection
#######################################################

def file_selector(folder_path):
    filenames = [file for file in os.listdir(folder_path) if file.endswith('.dat')]
    selected_filename = st.sidebar.selectbox('Select a file from folder above:', filenames)
    return os.path.join(folder_path, selected_filename)

st.sidebar.title("Select dataset")

path = st.sidebar.text_input(label="Folder path", value=PATH)
choosen_file = file_selector(path)

st.sidebar.markdown("""

------------------
""")

st.sidebar.title("Or upload a .dat file")
file = st.sidebar.file_uploader("", type=["dat", "csv"])
if file:
    choosen_file = file

df = load_data(choosen_file)
n, d = df.shape
MIN_EM, MAX_EM = df.columns.min(), df.columns.max()
MIN_EX, MAX_EX = df.index.min(), df.index.max()


#######################################################
#### Analytics
#######################################################

st.title('Excitation-Emission matrix analyzer')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.text('Excitation (rows) by Emissions (cols)')
    st.write(df)



st.header('Heatmap of EEM')

mask_ray = st.checkbox('Mask Rayleigh scatter?', value=True)
if mask_ray:
    mask_ray_width = st.number_input('Width of Rayleigh scatter masking (y = x ± width)', value=15)
else:
    mask_ray_width = 15

mask_raman = st.checkbox('Mask (aqueous) Raman scatter?')
log_scale = st.checkbox('Log scale?')
remove_upper_tri = st.checkbox('Remove upper triangle?', value=True)
normalize = st.checkbox('Normalize?', value=True)
ex_lb, ex_ub = st.slider("Excitation bounds (nm)", MIN_EX, MAX_EX, (MIN_EX, MAX_EX), step=(MAX_EX - MIN_EX)/(n-1))
em_lb, em_ub = st.slider("Emission bounds (nm)", MIN_EM, MAX_EM, (MIN_EM, MAX_EM), step=(MAX_EM - MIN_EM)/(d-1), key="2")

title = st.text_input(label="Set new title")

try:
    default_title = Path(choosen_file).name
except:
    default_title = ""


st.pyplot(eem_heatmap(df.loc[ex_ub:ex_lb].T.loc[em_lb:em_ub].T,
    rayleigh_scattering_mask_width=mask_ray_width if mask_ray else 0,
    raman_scattering_mask_width=10 if mask_raman else 0,
    log_scale=log_scale,
    plot_peaks=False,
    remove_upper_tri=remove_upper_tri,
    title=title or default_title,
    normalize=normalize,
    )[0],)

st.markdown("""Right-click and "Save image as..." to save.""")
