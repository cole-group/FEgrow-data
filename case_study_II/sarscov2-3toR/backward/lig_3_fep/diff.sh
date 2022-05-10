# check different mapping
for lm in *mapping ; 
do
	echo $lm ../com_2_fep/prot_${lm}
	diff -q $lm ../com_2_fep/prot_${lm}
	
done