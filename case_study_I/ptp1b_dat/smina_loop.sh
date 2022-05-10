#!/bin/bash
> smina_scores.dat
for i in 20667\_2qbp  23330\_2qbq  23469  23472  23475  23479  23483 20669\_2qbr  23466 23470  23473  23476  23480 20670\_2qbs  23468 23471  23474  23477  23482; do
	smina --score_only -l best_conformers_$i.pdb -r rec_h.pdb --seed 0 >> smina_scores.dat
done
