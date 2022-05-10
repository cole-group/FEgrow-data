export L=10 ; 
python combine.py --system1  ../lig_1_params/l"$L".prm7 ../lig_1_params/l"$L".rst7 --system2 ../prot_param/prot.prm7 ../prot_param/prot.rst7  --output prot_l"$L"
