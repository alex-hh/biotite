# This script superimposes the atom coordinates of the Ku70/80
# heterodimer onto the corresponding structure bound to DNA
# (superimposition of 1JEQ onto 1JEY).
# The visualisation was coducted with PyMOL.
# Orange: Ku dimer originally bound to DNA
# Green:  Free Ku dimer

import biotite
import biotite.structure as struc
import biotite.structure.io as strucio
import biotite.structure.io.pdbx as pdbx
import biotite.database.rcsb as rcsb
import numpy as np

# Download and parse structure files
file = rcsb.fetch("1JEY", "mmtf", biotite.temp_dir())
ku_dna = strucio.get_structure_from(file)
file = rcsb.fetch("1JEQ", "mmtf", biotite.temp_dir())
ku = strucio.get_structure_from(file)
# Remove DNA and water
ku_dna = ku_dna[(ku_dna.chain_id == "A") | (ku_dna.chain_id == "B")]
ku_dna = ku_dna[~struc.filter_solvent(ku_dna)]
ku = ku[~struc.filter_solvent(ku)]
# The structures have a differing amount of atoms missing
# at the the start and end of the structure
# -> Find common structure
ku_dna = ku_dna[struc.filter_intersection(ku_dna, ku)]
ku = ku[struc.filter_intersection(ku, ku_dna)]
# Superimpose
ku_superimposed, transformation = struc.superimpose(ku_dna, ku)
# Write PDBx files as input for PyMOL
cif_file = pdbx.PDBxFile()
pdbx.set_structure(cif_file, ku_dna, data_block="ku_dna")
cif_file.write("ku_dna.cif")
cif_file = pdbx.PDBxFile()
pdbx.set_structure(cif_file, ku_superimposed, data_block="ku")
cif_file.write("ku.cif")
# Visualisation with PyMOL...