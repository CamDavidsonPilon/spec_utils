# main.py


from utils import *
from plotting import *


df_h = eem_dat_file_to_df("~/Downloads/HotSauceH_trial2_EEM.dat")
df_ch = eem_dat_file_to_df("~/Downloads/HotSauceCH_trial2_EEM.dat")
# df_partial_h = eem_dat_file_to_df("~/Downloads/attachments (3)/HotSauceH_trial1_EEM.dat")

eem_heatmap(df_ch, rayleigh_scattering_mask_width=30)
eem_heatmap(df_ch, rayleigh_scattering_mask_width=30, log_scale=True)
eem_heatmap(df_h, rayleigh_scattering_mask_width=30, additional_mask=block_mask(df_h, "top" ,0.25))