#!/bin/bash
> gnina_scores.dat
for i in 2aa 2bb 2ee 2gg 2v 2x 2y 2z 3fln 3flq 3flw 3fly 3fmh 3fmk; do
	./gnina --score_only -l best_conformers_$i.sdf -r rec_h.pdb --seed 0 >> gnina_scores.dat
done

