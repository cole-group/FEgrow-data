import shutil
import os
from pathlib import Path


# copy the 
if not os.path.exists('Parameters'):
	shutil.copytree('../Parameters', 'Parameters')

cwd = Path(os.getcwd())
# L Begin, End
lB, lE = cwd.stem.split('-')
print('Ligands', lB, lE)

# copy the scripts
comsh = 'complex_lambdarun-comb.sh'
ligsh = 'ligand_lambdarun-comb.sh'
shutil.copy('../' + comsh, comsh)
shutil.copy('../' + ligsh, ligsh)


# prep the dir structure for com/lig:
# Perturbations/lx-ly/unbound/
# Perturbations/lx-ly/bound/

pert = Path('Perturbations')
pert.mkdir(exist_ok=True)
(pert / cwd.stem).mkdir(exist_ok=True)
(pert / cwd.stem / 'bound').mkdir(exist_ok=True)
(pert / cwd.stem / 'unbound').mkdir(exist_ok=True)

# copy lig fep
shutil.copy( Path('../') / 'lig_3_fep' / f'{lB}-{lE}.pert', pert / cwd.stem / 'unbound')
shutil.copy( Path('../') / 'lig_3_fep' / f'{lB}-{lE}.prm7', pert / cwd.stem / 'unbound')
shutil.copy( Path('../') / 'lig_3_fep' / f'{lB}-{lE}.rst7', pert / cwd.stem / 'unbound')

# copy com fep
shutil.copy( Path('../') / 'com_2_fep' / f'prot_{lB}-{lE}.pert', pert / cwd.stem / 'bound' / f'{lB}-{lE}.pert')
shutil.copy( Path('../') / 'com_2_fep' / f'prot_{lB}-{lE}.prm7', pert / cwd.stem / 'bound' / f'{lB}-{lE}.prm7')
shutil.copy( Path('../') / 'com_2_fep' / f'prot_{lB}-{lE}.rst7', pert / cwd.stem / 'bound' / f'{lB}-{lE}.rst7')