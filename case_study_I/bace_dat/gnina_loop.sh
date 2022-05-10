#!/bin/bash

for i in 13a 13b 13c 13d 13e 13f 13g 13h 13i 13j 13k 13m 13n 13o 17h; do
	gnina --score_only -l best_conformers_$i.sdf -r rec_h.pdb --seed 0 --stripH False >> gnina_scores.dat
done
