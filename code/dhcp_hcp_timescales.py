import nibabel as nib
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import optimize
import tau_estimation
from tau_estimation import run_tau_estimation
import brain_renders
from scipy.stats import spearmanr
import subprocess
#import rpy2.robjects as ro
import correlations

def plot_distribution(data,outname):
    sns.distplot(data)
    plt.savefig(outname)
    plt.close()

def corr_with_snr():
    r,p = spearmanr(snr, tau_mean)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (12,5))
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    ax.scatter(snr,tau_mean,alpha=0.5)
    #ax.set_ylim((10,35))
    ax.set_xlabel('Median SNR per ROI',fontsize = 12)
    ax.set_ylabel('Mean Tau per ROI (seconds)',fontsize = 12)
    ax.set_title(f'SNR vs Tau {group} \n r = {round(r,4)}, p = {round(p,4)}',fontsize = 12)
    plt.savefig(os.path.join(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/tau_corr_snr_{group}.png'), dpi=300)
    plt.show()
    plt.close()

#def friedman_test(data):
#    r=ro.r
#    r.source('friedman_test.r')
#    p=r.rtest(data)
#    return p


#groups_list = ['dhcp_group1','dhcp_group2','hcp']
groups_list = ['hcp']

run_within_analysis = False
run_tau_estimation_analysis = False
run_brainrenders = False
run_between_analysis = True

###########################
### Within group analysis #
###########################
if run_within_analysis:

    for group in groups_list:
        if 'dhcp' in group:
            TR = 0.392
        else:
            TR = 1.97

        subj_file = pd.read_csv(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/data/{group}_subj_list.csv')
        subj_list = list(subj_file.iloc[:,0])
        if run_tau_estimation_analysis:
            run_tau_estimation(group, subj_list)

        # load tau file
        tau = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_{group}.txt')
        
        # remove outliers
        p95_tau = np.nanpercentile(tau,95)
        tau[np.where(tau>p95_tau)] = np.nan

        # multiply by TR to get the scale in seconds, plot distribution, and calculate friedman test
        tau = tau * TR
        plot_distribution(tau,f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/tau_distribution_{group}.png')

        tau_mean = np.nanmean(tau,axis=0)
        np.savetxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_ROImean_{group}.txt',tau_mean)
        # check correlation to snr and plot
        if 'group1' in group:
            snr = np.loadtxt(os.path.join('/dhcp/fmri_anna_graham/dhcp_hcp_timescales/data/sub-CC00058XX09_ses-11300_preproc_bold-snr-mean_individualspace.txt'))
            corr_with_snr()
        
        # get data for brain rendering
        if run_brainrenders:
            brain_renders.brainrenders(group,tau_mean)

        ##TODO: can we implement Friedman test here in python?
        # 2. barplots by net


############################
### Between group analysis #
############################
if run_between_analysis:
    dhcp_group1 = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_ROImean_dhcp_group1.txt')
    dhcp_group2 = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_ROImean_dhcp_group2.txt')
    snr = np.loadtxt(os.path.join('/dhcp/fmri_anna_graham/dhcp_hcp_timescales/data/sub-CC00058XX09_ses-11300_preproc_bold-snr-mean_individualspace.txt'))
    hcp = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_ROImean_hcp.txt')

    correlations.run_and_plot_corr(dhcp_group1,dhcp_group2,'dhcp_group1','dhcp_group2',f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/corr_dhcp1_dhcp2.png')
    #correlations.run_and_plot_partial_corr(dhcp_group1,dhcp_group2,snr,f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/partial_corr_dhcp1_dhcp2_snr.csv')
    correlations.run_and_plot_corr(hcp,dhcp_group1,'hcp','dhcp_group1',f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/corr_dhcp1_hcp.png')
    correlations.run_and_plot_corr(hcp,dhcp_group2,'hcp','dhcp_group2',f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/corr_dhcp2_hcp.png')


    # TODO:
    # 1. corr between dhcp groups (both direct and partialling out snr)
    # 2. corr between hcp and each dhcp group (both whole brain and single nets)
    # 3. transmodal vs unimodal comparison




    #outlier_upper_lim = np.mean(tau)+2*np.std(tau)
    #tau[np.where(tau>outlier_upper_lim)] = np.nan
    #tau[np.where(tau<0)] = np.nan
    
    #friedman_res = friedman_test(tau)
    #print(friedman_res)
