import nibabel as nib
import numpy as np 
import os
from scipy import optimize
import pandas as pd

def autocorr_decay(dk,A,tau,B):
    return A*(np.exp(-(dk/tau))+B)

def run_tau_estimation(group,subj_list,**kwargs):
    roi=400
    alltau = np.zeros((len(subj_list),roi))
    nlags = 100
    removelag0 = 1
    if 'dhcp' in group:
        root_pth = '/dhcp/fmri_anna_graham/timecourses'
    else:
        root_pth = '/camcan/schaefer_parc/'

    for i,sub in enumerate(subj_list):
        print(sub)
        if 'dhcp' in group:
            sub_id = sub.split('\'')[1]
            sess_id = sub.split('\'')[3]
            filename = os.path.join(root_pth,f'{sub_id}/{sess_id}/{sub_id}_{sess_id}_task-rest_bold.txt')
        else:
            filename = os.path.join(root_pth,f'camcan_rest_{sub}_fd.txt')
        ts_df = np.loadtxt(filename)
        xdata=np.arange(nlags)

        autocorr_values = np.zeros((ts_df.shape[1], nlags))
        for ROI in range(0,ts_df.shape[1]):
            xc=ts_df[:,ROI]-np.mean(ts_df[:,ROI])
            fullcorr=np.correlate(xc, xc, mode='full')
            fullcorr=fullcorr / np.max(fullcorr)
            start=len(fullcorr) // 2
            stop=start+nlags
            autocorr_values[ROI,:]=fullcorr[start:stop]        

        for ROI in range(0,ts_df.shape[1]):
            try:
                A, tau, B = optimize.curve_fit(autocorr_decay,xdata[removelag0:],autocorr_values[ROI,removelag0:],p0=[0,np.random.rand(1)[0]+0.01,0],bounds=(([0,0,-np.inf],[np.inf,np.inf,np.inf])),method='trf',maxfev=1000)[0]
                alltau[i,ROI] = tau
            except:
                alltau[i,ROI] = np.nan

    print(alltau.shape)
    np.savetxt(f'/dhcp/fmri_anna_graham/dhcp_camcan_timescales/results/tau_estimation_{group}.txt',alltau)

    tau_df=pd.DataFrame(data=alltau[0:,0:],
            index=[i for i in range(alltau.shape[0])],
            columns=[i for i in range(alltau.shape[1])])
    tau_df.insert(loc=0, column='subj', value=[item[0] for item in subj_list])
    tau_df.insert(loc=1, column='sess', value=[item[1] for item in subj_list])
    tau_df.to_csv(f'/dhcp/fmri_anna_graham/dhcp_camcan_timescales/results/tau_estimation_{group}.csv')
