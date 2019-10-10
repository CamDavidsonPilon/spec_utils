# main.py


from utils import *
from plotting import *


df_first_trial = eem_dat_file_to_df("~/Downloads/HotSauceCH_trial2_EEM.dat")
df_second_trial = eem_dat_file_to_df(
    "~/Downloads/attachments (4)/HotSauceH_trial3_EEM.dat"
)

eem_heatmap(df_first_trial, rayleigh_scattering_mask_width=25)


df_dw = eem_dat_file_to_df("~/Downloads/attachments (4)/HotSauceDW_trial3_EEM.dat")
df_second_trial_with_blank = eem_dat_file_to_df(
    "~/Downloads/attachments (4)/HotSauceH_w_blank_trial3_EEM.dat"
)


eem_heatmap(
    df_second_trial_with_blank, rayleigh_scattering_mask_width=25, log_scale=True
)
eem_heatmap(df_second_trial, rayleigh_scattering_mask_width=25, log_scale=True)
