setwd('/dhcp/fmri_anna_graham/dhcp_camcan_timescales/results/')

### dhcp_group1
db <- read.csv('tau_estimation_dhcp_group1.txt', sep='\t')
friedman.test(as.matrix(db))

### dhcp_group1
db <- read.csv('tau_estimation_dhcp_group2.txt', sep='\t')
friedman.test(as.matrix(db))
