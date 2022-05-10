#!/bin/bash

for i in {11..41}; do
        obabel -ipdb best_conformers_$i.pdb -osdf -O best_conformers_$i.sdf 
done

