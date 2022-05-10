#!/bin/bash
> gnina_scores.dat
for i in {11..41}; do
        ./gnina --score_only -l best_conformers_$i.sdf -r rec_h.pdb --seed 0 >> gnina_scores.dat
done

