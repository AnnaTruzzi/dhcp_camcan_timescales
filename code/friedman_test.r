#setwd('/dhcp/fmri_anna_graham/dhcp_camcan_timescales/results/')
setwd('C:/Users/Anna/Documents/Research/Projects/ONGOING/Project dHCP_Autocorrelation/dhcp_camcan_timescales/results')

### dhcp_group1
db <- read.csv('tau_estimation_dhcp_group1.csv', sep=',')
db_tau <- db[,4:403]
p95 <- quantile(db_tau,.95,na.rm=TRUE)
db_tau[db_tau>p95] <- NA
friedman.test(as.matrix(db_tau))



### dhcp_group2
db <- read.csv('tau_estimation_dhcp_group2.csv', sep=',')
friedman.test(as.matrix(db[,4:403]))
db_tau <- db[,4:403]
p95 <- quantile(db_tau,.95,na.rm=TRUE)
db_tau[db_tau>p95] <- NA
friedman.test(as.matrix(db_tau))

