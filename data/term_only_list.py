import numpy as np 
import pandas as pd 
import os

infopth = '/dhcp/fmri_anna_graham/dhcp_hcp_timescales/data' 
dhcp_info = pd.read_csv(os.path.join(infopth,'participants_dhcp.txt'), sep='\t')

term_only = dhcp_info[dhcp_info['birth_age']>36]['participant_id']

term_only.to_csv('/dhcp/fmri_anna_graham/dhcp_hcp_timescales/data/dhcp_term_only_list.csv')
