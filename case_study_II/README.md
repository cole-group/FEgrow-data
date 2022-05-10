## rgroup-case-sarscov2-3toR
RBFE input files for the reproduction of the study case sarscov2-3toR in the `rgroup` package. 

## BioSimSpace protocols and scripts used to generate the input files for FEP calculations. 

The following details the procedure for protein-ligand binding free energy calculations. 

## File Setup for Free Energy Calculations

Install BioSimSpace (https://github.com/michellab/BioSimSpace/)

### 1a) Parameterise the protein with **AMBER** forcefield:
  - Given the protein in pdb format, use the [parameterise.py](https://github.com/michellab/BioSimSpace/blob/devel/nodes/playground/parameterise.py) script from BioSimSpace to parameterise it with the ff14SB amber forcefield, and generating .rst7 and .prm7 files: ```parameterise.py --input FILE.pdb --forcefield ff14SB --output FILE```
  - save the generated .rst7 and .prm files in the `1.prot_param` directory

### 1b) Generate AMBER format forcefield for the ligands (GAFF):
  - Given a molecule in a pdb format in `lig_0_initial_pdb` directory, use ```parameterise.py --input MOL.pdb --forcefield GAFF2 --output MOL```
  - Save each molecule's .rst7 and .prm in `lig_1_params`

### 2) Combine each ligand and protein:
  - for each ligand, combine it with the protein: ```combine.py --system1 MOL.prm7 MOL.rst7 --system2 PROTEIN.prm7 PROTEIN.rst7 --output PROT_MOL``` in the `com_0_params` directory
  - this will create unsolvated prm7 and rst7 files

### 3a) Solvate the ligands:
  - solvate each of the ligand files with ```solvate.py --input MOL.prm7 MOL.rst7 --output MOL_sol --water tip3p --box_dim 35``` in the `lig_2_soleq`
  - `--box_dim` is the box size used for our system in Angstroms
  
### 3b) Solvate the complex:
  - solvate the prm7 and rst7 files of the complxes: ```solvate.py --input PROT_MOL.prm7 PROT_MOL.rst7 --output PROT_MOL_sol --water tip3p --box_dim 90``` in the `com_1_soleq` directory
  - `--box_dim` is the box size used for our system in Angstroms

### 4) Equilibrate the solvated systems:
```
   WARNING: Equilibration should be used after generating the FEP files which decide on which atoms will be morphed in each transformation. Otherwise, some of the morphing atoms across the two RBFE legs might not be the same. Here we used a workaround. Please see our updated protocols or aply equilibration after FEP preparation. 
```

  - equilibrate the _sol.rst7 files for the bound and unbound systems (e.g. mol_sol_eq.rst7 or prot_mol_sol_eq.rst7): ```amberequilibration.py --input MOL_sol.prm7 MOL_sol.rst7 --output MOL_soleq``` in both `lig_2_soleq` and `com_1_soleq` directories. Note the new suffix `_soleq`.

### 5) Generate the files for the free energy calculations:

  - create the perturbation files for the free energy calculations (e.g. for a transition of Lig1 to Lig2 the above command will create .mapping, .mergeat0.pdb. .pert, .prm7 and .rst7 files for this pertubration). Use this command for both bound and unbound environments: ```prepareFEP.py --input1 PROT_MOL_soleq.prm7 PROT_MOL_soleq.rst7 --input2 PROT_MOL_soleq.prm7 PROT_MOL_soleq.rst7 --output PROT_MOL1_to_MOL2``` in the `com_2_fep` directory. 
  - In order to ensure that the same perturbation is used for both of the RBFE legs, modify the `prepareFEP.py` script to load the mapping from the complex, and then use it in the `lig_3_fep`. See the warning above to avoid this workaround. 

### 6) Free Energy Calculations
Copy the directory `Parameters` and the scripts `complex_lambdarun-comb.sh` and `ligand_lambdarun-comb.sh` into the main directory. The `Parameters` folder contains the main configuration file `lambda.cfg`.

For each transformation:
1) Create a directory named `MOL1-MOL2`. In the directory run `python ../init.py` to initialise the directory. 
2) The lambda.cfg file contains various parameters, namely the number of moves and cycles, the timestep, the type of constraints, the lambda windows used and the platform on which to run the calculation. 
3) Run the ```ligand_lambdarun-comb.sh``` and ```complex_lambdarun-comb.sh``` scripts
- Script ```ligand_lambdarun-comb.sh``` runs the command for the unbound perturbations, whilst ```complex_lambdarun-comb.sh``` runs the bound perturbations. 
4) Gather the results by runing ```analyse_freenrg mbar -i lambda-*/simfile.dat -o out.dat -p 90``` in all discharge and vanish directories. 

## Results

In addition to the above instructions for generating the input files for this paper, the `results` directory also contains the raw data (free energy calculations) which can be analysed with ```python run_networkanalysis.py sars/sarscov2-3toR.csv --target_compound 14 -o sars.dat -e sars/sarscov2_ic50_exp.csv --stats --generate_notebook```.

This protocol was carried out in both `forward` and `backward` directories counting effectively as two replicas. 


