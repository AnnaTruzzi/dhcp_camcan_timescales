#!/bin/bash

#SBATCH -J dhcp_hcp_timescales
#SBATCH --output=/dhcp/fmri_anna_graham/dhcp_hcp_timescales/logs/slurm-%j.out
#SBATCH --error=/dhcp/fmri_anna_graham/dhcp_hcp_timescales/logs/slurm-%j.err

PYTHON="/home/annatruzzi/anaconda3/bin/python"

${PYTHON} /dhcp/fmri_anna_graham/dhcp_hcp_timescales/code/dhcp_hcp_timescales.py