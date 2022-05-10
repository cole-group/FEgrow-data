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
		--input1 ../lig_2_soleq/l"$LB"_sol.prm7 ../lig_2_soleq/l"$LB"_soleq.rst7 \
		--input2 ../lig_2_soleq/l"$LE"_sol.prm7 ../lig_2_soleq/l"$LE"_soleq.rst7 \
		--output l"$LB"-l"$LE" -v
		""")