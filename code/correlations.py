import numpy as np 
import pandas as pd 
import os
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from statsmodels.regression import linear_model
from pingouin import partial_corr


def run_and_plot_corr(x,y,x_label,y_label,plotname,title=None,xlim=15, ylim=15):
    r,p = spearmanr(x,y)
    plt.scatter(x, y,alpha=0.5,s=10)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.xlabel(f'{x_label} - Tau (seconds)', fontsize = 12)
    plt.ylabel(f'{y_label} - Tau (seconds)', fontsize = 12)
    plt.xlim((0,xlim))
    plt.ylim((0,ylim))
    if title:
        plt.suptitle(f'{title} \n r = {round(r,4)}, p = {round(p,4)}')
    else:
        plt.suptitle(f'r = {round(r,4)}, p = {round(p,4)}')
        
    plt.savefig(plotname)
    #plt.show()
    plt.close()

def run_and_plot_partial_corr(x,y,covar,outname):
    cor_dict = {'x': x,
                'y': y,
                'covar': covar}
    cor_df = pd.DataFrame(cor_dict)
    res = partial_corr(data=cor_df, x='x', y='y', covar='covar', method='spearman')
    res.to_csv(outname)


def run_and_plot_corr_bynet(x,y,x_label,y_label,net_dict,xlim=15, ylim=15):
    for i,net in enumerate(net_dict.keys()):
        net_idx=net_dict[net]
        r,p = spearmanr(x[net_idx],y[net_idx])
        plt.scatter(x[net_idx], y[net_idx],alpha=0.5,s=10)
        plt.xticks(fontsize = 10)
        plt.yticks(fontsize = 10)
        plt.xlabel(f'{x_label} - Tau (seconds)', fontsize = 12)
        plt.ylabel(f'{y_label} - Tau (seconds)', fontsize = 12)
        plt.xlim((6,15))
        plt.suptitle(f'{net} \n r = {round(r,4)}, p = {round(p,4)}')
        plt.savefig(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/corr_{x_label}_{y_label}_{net}_7net.png')
        plt.savefig(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/corr_{x_label}_{y_label}_{net}_7net.pdf')
        #plt.show()
        plt.close()