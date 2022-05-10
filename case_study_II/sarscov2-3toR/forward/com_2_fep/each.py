import glob
import os

perts = glob.glob('../l*-l*')
print(perts)
for pert in perts:
	l, r = pert.split('-')
	l = l.split('l')[-1]
	r = r.split('l')[-1]
	print(l, r)

	os.system(f"""
	LB={l} ; LE={r} ; 
	python prepareFEP.py \
		--input1 ../com_1_soleq/prot_l"$LB"_sol.prm7 ../com_1_soleq/prot_l"$LB"_soleq.rst7 \
		--input2 ../com_1_soleq/prot_l"$LE"_sol.prm7 ../com_1_soleq/prot_l"$LE"_soleq.rst7 \
		--output prot_l"$LB"-l"$LE" -v
		""")
