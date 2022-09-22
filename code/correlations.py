import numpy as np 
import pandas as pd 
import os
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from statsmodels.regression import linear_model
#from pingouin import partial_corr


def run_and_plot_corr(x,y,x_label,y_label,plotname):
    r,p = spearmanr(x,y)
    plt.scatter(x, y,alpha=0.5,s=10)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.xlabel(f'{x_label} - Tau (seconds)', fontsize = 12)
    plt.ylabel(f'{y_label} - Tau (seconds)', fontsize = 12)
    plt.xlim((0,15))
    plt.suptitle(f'r = {round(r,4)}, p = {round(p,4)}')
    plt.savefig(plotname)
    #plt.show()
    plt.close()

def run_and_plot_partial_corr(x,y,covar,x_label,y_label,covar_name):
    cor_dict = {'x': x,
                'y': y,
                'covar': covar}
    cor_df = pd.DataFrame(cor_dict)
    res = partial_corr(data=cor_df, x='x', y='y', covar='covar', method='spearman')
    res.to_csv(f'C:\\Users\\Anna\\Documents\\Research\\Projects\\ONGOING\\Project dHCP_Autocorrelation\\MRIautocorr_ARMA\\Docs\\corr_dhcp_group1AND2_partialcorr.txt',sep='\t')
