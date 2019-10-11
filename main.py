# main.py


from utils import *
from plotting import *


df_dw = eem_dat_file_to_df("~/Downloads/attachments (4)/HotSauceDW_trial3_EEM.dat")
df_second_trial_with_blank = eem_dat_file_to_df(
    "~/Downloads/attachments (4)/HotSauceH_w_blank_trial3_EEM.dat"
)

fig, ax = eem_heatmap(df_dw, rayleigh_scattering_mask_width=25, raman_scattering_mask_width=5, remove_upper_tri=True)
plt.show()