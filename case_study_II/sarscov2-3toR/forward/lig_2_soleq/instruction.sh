L=10
python solvate.py --input ../lig_1_params/l"$L".prm7 ../lig_1_params/l"$L".rst7 --output l"$L"_sol --water tip3p --box_dim 35
python amberequilibration.py --input l"$L"_sol.prm7 l"$L"_sol.rst7 --output l"$L"_soleq
