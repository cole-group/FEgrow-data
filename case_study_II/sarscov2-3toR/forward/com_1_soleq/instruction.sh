export L=10
python solvate.py --input ../com_0_params/prot_l"$L".prm7 ../com_0_params/prot_l"$L".rst7 --output prot_l"$L"_sol --water tip3p --box_dim 90
python amberequilibration.py --input l"$L"_sol.prm7 l"$L"_sol.rst7 --output l"$L"_soleq
