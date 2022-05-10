#!/usr/bin/env python
# coding: utf-8

# Author: Julien Michel
# 
# email: julien.michel@ed.ac.uk

# # PrepareFEP
# Loads a pair of input files, perform mapping between the first molecule of each input. Write down input files for a SOMD FEP calculation.

# In[1]:


import BioSimSpace as BSS
import os
from Sire.Mol import AtomIdx
import shutil


# In[2]:


def writeLog(ligA, ligB, mapping, output):
    """ Human readable report on atoms used for the mapping."""
    atoms_in_A = list(mapping.keys())
    stream = open(output,'w')
    atAdone = []
    atBdone= []
    for atAidx in atoms_in_A:
        # breakpoint()
        # import ipdb ; ipdb.set_trace()
        atA = ligA._getSireObject().select(AtomIdx(atAidx))
        atB = ligB._getSireObject().select(AtomIdx(mapping[atAidx]))
        stream.write("%s %s --> %s %s\n" % (atA.index(), atA.name(),atB.index(), atB.name()))
        atAdone.append(atA)
        atBdone.append(atB)
    for atom in ligA._getSireObject().atoms():
        if atom in atAdone:
            continue
        stream.write("%s %s --> dummy\n" % (atom.index(), atom.name()))
    for atom in ligB._getSireObject().atoms():
        if atom in atBdone:
            continue
        stream.write("dummy --> %s %s\n" % (atom.index(), atom.name()))
    stream.close()


# In[3]:


def loadMapping(mapping_file):
    """Parse a text file that specifies mappings between atomic indices in input1 --> atoms in input2"""
    stream = open(mapping_file,'r')
    buffer = stream.readlines()
    stream.close()
    mapping = {}
    for line in buffer:
        if line.startswith("#"):
            continue
        elems = line.split(",")
        idx1 = int(elems[0])
        idx2 = int(elems[1])
        mapping[ AtomIdx(idx1)] = AtomIdx(idx2)
    
    return mapping


# In[4]:


node = BSS.Gateway.Node("A node to generate input files for a SOMD relative free energy calculation.")


# In[5]:


node.addAuthor(name="Julien Michel", email="julien.michel@ed.ac.uk", affiliation="University of Edinburgh")
node.setLicense("GPLv3")


# In[6]:


node.addInput("input1", BSS.Gateway.FileSet(help="A topology and coordinates file"))
node.addInput("input2", BSS.Gateway.FileSet(help="A topology and coordinates file"))
node.addInput("prematch", BSS.Gateway.String(help="list of atom indices that are matched between input2 and input1. Syntax is of the format 1-3,4-8,9-11... Ignored if a mapping is provided", default=""))
node.addInput("mapping", BSS.Gateway.File(help="csv file that contains atom indices in input1 mapped ot atom indices in input2", optional=True))
node.addInput("output", BSS.Gateway.String(help="The root name for the files describing the perturbation input1->input2."))


node.addOutput("nodeoutput", BSS.Gateway.FileSet(help="SOMD input files for a perturbation of input1->input2."))


node.showControls()


do_mapping = True
custom_mapping = node.getInput("mapping")
#print (custom_mapping)
if custom_mapping is not None:
    do_mapping = False
    mapping = loadMapping(custom_mapping)
    #print (mapping)


# Optional input, dictionary of Atom indices that should be matched in the search. 
prematch = {}
prematchstring = node.getInput("prematch")
if len(prematchstring) > 0: 
    entries = prematchstring.split(",")
    for entry in entries:
        idxA, idxB = entry.split("-")
        prematch[ AtomIdx( int(idxA)) ] = AtomIdx( int(idxB) )
#print (prematch)


# Load system 1
system1 = BSS.IO.readMolecules(node.getInput("input1"))

# Load system 2
system2 = BSS.IO.readMolecules(node.getInput("input2"))

# We assume the molecules to perturb are the first molecules in each system
lig1 = system1.getMolecules()[0]
lig2 = system2.getMolecules()[0]


if do_mapping:
    # Return a maximum of 10 matches, scored by RMSD and sorted from best to worst.
    print('prematch', prematch)
    mappings, scores = BSS.Align.matchAtoms(lig1, lig2, matches=10, prematch=prematch, return_scores=True, complete_rings_only=True, scoring_function="RMSDalign", timeout=10*BSS.Units.Time.second)
    print('file align', BSS.Align.__file__)
    # We retain the top mapping
    mapping = mappings[0]
    #print (len(mappings))
    #print (mappings)


#print (mapping)
#for x in range(0,len(mappings)):
#    print (mappings[x], scores[x])

# check if there is a mapping already done in the ligand, 
# if that's the case, take that instead,
# import os, re
# lb, le = os.environ['LB'], os.environ['LE']
# from pathlib import Path

# if 'com_2_fep' in os.getcwd():
#     print('fresh')
# else:
#     lig_map = Path(os.getcwd()).parent / 'com_2_fep' / f'prot_l{lb}-l{le}.mapping'
#     # from the following line like extraact indices
#     # AtomIdx(19) AtomName('CL1') --> AtomIdx(19) AtomName('CL1')

#     lig_mapping = {}
#     for l in open(lig_map).readlines():
#         idx = re.findall(r'AtomIdx\((\d+)\).*AtomIdx\((\d+)\).*', l)
#         if not idx or len(idx[0]) != 2:
#             continue
#         idfrom, idto = int(idx[0][0]), int(idx[0][1])
#         print(idfrom, idto)
#         lig_mapping[idfrom] = idto

#     print('before', mapping)
#     mapping = lig_mapping
#     print('mapping for the align stage', mapping)

# mapping = {0: 0, 1: 1, 12: 12, 2: 2, 4: 4, 10: 10, 15: 15, 16: 16, 14: 14, 18: 18, 5: 5, 6: 6, 7: 7, 8: 8, 17: 17, 9: 9, 26: 26, 25: 25, 24: 24, 23: 23, 28: 28, 29: 29, 30: 30, 31: 31, 32: 32, 33: 33, 34: 34, 36: 36, 39: 39, 35: 35, 38: 38, 37: 37, 22: 22, 3: 3, 13: 13, 11: 11, 27: 27, 53: 50, 46: 47, 45: 44, 40: 41, 41: 42, 47: 43, 44: 45, 52: 48, 54: 49, 21: 21, 20: 20, 19: 19}

# [mapping.pop(x) for x in [45, 44, 40, 47, 41]]

inverted_mapping = dict([[v,k] for k,v in mapping.items()])
#print (inverted_mapping)


# Align lig2 to lig1 based on the best mapping (inverted). The molecule is aligned based
# on a root mean squared displacement fit to find the optimal translation vector
# (as opposed to merely taking the difference of centroids).
lig2 = BSS.Align.rmsdAlign(lig2, lig1, inverted_mapping)
# Merge the two ligands based on the mapping.
merged = BSS.Align.merge(lig1, lig2, mapping) #, allow_ring_breaking=True)
# Create a composite system
system1.removeMolecules(lig1)
system1.addMolecules(merged)


# In[18]:

root = node.getInput("output")
mapping_str = "%s.mapping" % root

# Log the mapping used
writeLog(lig1, lig2, mapping, output=mapping_str)
BSS.IO.saveMolecules(f"{root}.mergeat0.pdb", merged, "pdb", { "coordinates" : "coordinates0" })
# BSS.IO.saveMolecules("merged_at_lam0.pdb", merged, "pdb", { "coordinates" : "coordinates0" , "element": "element0" })
# Generate package specific input
protocol = BSS.Protocol.FreeEnergy(runtime = 2*BSS.Units.Time.nanosecond, num_lam=3)
#protocol = BSS.Protocol.FreeEnergy(runtime = 2*BSS.Units.Time.femtosecond, num_lam=3)
process = BSS.Process.Somd(system1, protocol)
process.getOutput() # creates the .zip? 
shutil.move('somd_output.zip', f'{root}.zip')

# we copy them directl from _work_dir ?
# cmd = "unzip -o somd_output.zip"
# os.system(cmd)

root = node.getInput("output")
pert = "%s.pert" % root
prm7 = "%s.prm7" % root
rst7 = "%s.rst7" % root

# fixme - shutil? 
cmd = f"""  mv {process._work_dir}/somd.pert {pert} ; 
            mv {process._work_dir}/somd.prm7 {prm7} ; 
            mv {process._work_dir}/somd.rst7 {rst7} ; 
       """
os.system(cmd)


node.setOutput("nodeoutput",[pert, prm7, rst7, mapping_str])
node.validate()