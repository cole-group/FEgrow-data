import numpy as np

ic_raw = np.loadtxt('sarscov2_ic50_exp.csv', delimiter=',',
	dtype={'names': ('id', 'ic50'), 'formats': ('i4', 'f4')}
	)
ddgs = np.loadtxt('sarscov2-3toR.csv', delimiter=',', 
	dtype={'names': ('idfrom', 'idto', 'ddg', 'err'), 'formats': ('i4', 'i4', 'f4', 'f4')}
	)

ic = {i:ic50 for i, ic50 in ic_raw}


ddg_means = []
ddg_exps = []
for i in range(0, len(ddgs), 2):
	idfrom, idto, ddg, err = ddgs[i]
	print('ddg', idfrom, idto, ddg)
	idfrom_rev, idto_rev, ddg_rev, err_rev = ddgs[i+1]
	assert idto==idfrom_rev and idfrom==idto_rev
	
	# average the A:B and B:A
	ddg_mean = np.mean([ddg,-ddg_rev])

	# get experimental
	ddg_exp = 0.0019872041 * 300 * np.log(ic[idto]/ic[idfrom])
	print('exp', ddg_exp)

	ddg_means.append(ddg_mean)
	ddg_exps.append(ddg_exp)

rmse = np.sqrt(np.mean(np.square(np.array(ddg_means) - np.array(ddg_exps))))
print('rmse', rmse)