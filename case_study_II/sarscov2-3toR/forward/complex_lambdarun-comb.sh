export SIRE_DONT_PHONEHOME=1

for hdir in `find Perturbations/* -type d -name "l*-l*"`
do
	echo "Complex hybird dir $hdir"
	# remove the Perturbations/ prefix
	hyb=${hdir#Perturbations/}

	cd Perturbations/$hyb/bound
	for lam in $(seq 0.0 0.1 1.0);
	do 
		mkdir lambda-${lam}
		cd lambda-${lam}
			somd-freenrg -t ../$hyb.prm7 -c ../$hyb.rst7 -m ../$hyb.pert -C ../../../../Parameters/lambda.cfg -l $lam ;
			echo "		=======================\ndone $c  lambda $s 	\n======================="
		cd ../ ;
	done
done