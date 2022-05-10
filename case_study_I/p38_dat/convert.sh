#!/bin/bash

for i in 2aa 2bb 2ee 2gg 2v 2x 2y 2z 3fln 3flq 3flw 3fly 3fmh 3fmk; do        
	obabel -ipdb best_conformers_$i.pdb -osdf -O best_conformers_$i.sdf
done

