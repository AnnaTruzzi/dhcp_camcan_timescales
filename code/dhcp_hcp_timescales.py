import nibabel as nib
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import optimize
from unimodal_vs_transmodal import unimodal_vs_transmodal
import tau_estimation
from tau_estimation import run_tau_estimation
import brain_renders
from scipy.stats import spearmanr
import subprocess
#import rpy2.robjects as ro
import correlations
import pickle  

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


def get_net_dict():
    network_file17 = pd.read_csv('/dhcp/fmri_anna_graham/dhcp_hcp_timescales/data/Schaefer2018_400Parcels_17Networks_order.txt',sep = '\t', header = None)
    roi_names_all = np.array(network_file17[1])
    net_list = np.unique(np.array([i.split('_')[2][0:3] for i in roi_names_all]))
    myorder = [4,5,3,0,1,2,6,7]
    net_list = [net_list[i] for i in myorder]
    tem_index = [i for i, v in enumerate(net_list) if 'Tem' in v]
    net_list[6] = 'TempPar'
    print(net_list)
    net_dict = {}
    for netnum,net in enumerate(net_list):
        net_dict[net] = []
        for i,roi in enumerate(roi_names_all):
            if net in roi:
                net_dict[net].append(i)    
    return net_dict

#def friedman_test(data):
#    r=ro.r
#    r.source('friedman_test.r')
#    p=r.rtest(data)
#    return p


groups_list = ['dhcp_group1','dhcp_group2','hcp']

snr = np.loadtxt('/dhcp/fmri_anna_graham/dhcp_hcp_timescales/data/sub-CC00058XX09_ses-11300_preproc_bold-snr-mean_individualspace.txt')
net_dict = get_net_dict()
low_snr_idx = np.where(snr<40)[0]
high_snr_index = np.where(snr>=40)[0]
net_dict = get_net_dict()


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
        
        # remove outliers and multiply by TR
        p95_tau = np.nanpercentile(tau,95)
        tau[np.where(tau>p95_tau)] = np.nan
        tau = tau * TR
        np.savetxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_in_seconds_{group}.txt',tau)

        # plot distribution
        plot_distribution(tau,f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/tau_distribution_{group}.png')
        plt.style.use('classic')
        im = plt.imshow(tau)
        plt.colorbar(im)
        plt.savefig(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/tau_2Ddist_{group}.png')
        plt.close()

        tau_mean = np.nanmean(tau,axis=0)
        np.savetxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_ROImean_{group}.txt',tau_mean)
        # check correlation to snr and plot

        if 'group1' in group:
            corr_with_snr()
        
        # get data for brain rendering
        if run_brainrenders:
            brain_renders.brainrenders(group,tau_mean,net_dict,low_snr_idx)


        net_name_list_plot=[]
        tau_bynet_plot = []
        for net in net_dict.keys():
            net_name_list_plot.extend(np.repeat(net,len(net_dict[net])))
            tau_bynet_plot.extend(tau_mean[net_dict[net]])
        plot_bynet_dict = {'net_name':net_name_list_plot,'tau':tau_bynet_plot}
        plot_bynet_df = pd.DataFrame(plot_bynet_dict)
        sns.barplot(data=plot_bynet_df, x='net_name', y='tau')
        plt.savefig(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/tau_bynet_{group}.png')
        plt.close()


        ##TODO: can we implement Friedman test here in python?



############################
### Between group analysis #
############################
if run_between_analysis:
    dhcp_group1 = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_in_seconds_dhcp_group1.txt')
    dhcp_group2 = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_in_seconds_dhcp_group2.txt')
    hcp = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_in_seconds_hcp.txt')

    dhcp_group1_mean = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_ROImean_dhcp_group1.txt')
    dhcp_group2_mean = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_ROImean_dhcp_group2.txt')
    hcp_mean = np.loadtxt(f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/tau_estimation_ROImean_hcp.txt')


    correlations.run_and_plot_corr(dhcp_group1_mean,dhcp_group2_mean,'dhcp_group1','dhcp_group2',f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/corr_dhcp1_dhcp2.png')
    #correlations.run_and_plot_partial_corr(dhcp_group1,dhcp_group2,snr,f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/results/partial_corr_dhcp1_dhcp2_snr.csv')
    correlations.run_and_plot_corr(hcp_mean[high_snr_index],dhcp_group1_mean[high_snr_index],'hcp','dhcp_group1',f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/corr_dhcp1_hcp_highSNR.png')
    correlations.run_and_plot_corr(hcp_mean[high_snr_index],dhcp_group2_mean[high_snr_index],'hcp','dhcp_group2',f'/dhcp/fmri_anna_graham/dhcp_hcp_timescales/figures/corr_dhcp2_hcp_highSNR.png')


    # Corr by net
    correlations.run_and_plot_corr_bynet(hcp_mean,dhcp_group1_mean,'hcp','dhcp_group1',net_dict)
    correlations.run_and_plot_corr_bynet(hcp_mean,dhcp_group2_mean,'hcp','dhcp_group2',net_dict)


    with open('/dhcp/fmri_anna_graham/dhcp_hcp_timescales/data/roi_by_netclass.pickle','rb') as f:
        network_file_Ito = pickle.load(f)
    unimodal_index = [i-1 for i in network_file_Ito['unimodal']]
    transmodal_index = [i-1 for i in network_file_Ito['transmodal']]


    unimodal_vs_transmodal(dhcp_group1,hcp,unimodal_index,transmodal_index,'dhcp_group1','hcp')
    unimodal_vs_transmodal(dhcp_group2,hcp,unimodal_index,transmodal_index,'dhcp_group2','hcp')




    #outlier_upper_lim = np.mean(tau)+2*np.std(tau)
    #tau[np.where(tau>outlier_upper_lim)] = np.nan
    #tau[np.where(tau<0)] = np.nan
    
    #friedman_res = friedman_test(tau)
    #print(friedman_res)
