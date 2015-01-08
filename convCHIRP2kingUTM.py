#Convert all txt files in Leah's folder, LaJolla/nav/LINES, to UTM kingdom files
#for SONGS project
#V.J.Sahakian 11 November 2014

import numpy as np
from os import path
import chirpNav
from glob import glob

#Read in all paths
chirpPaths=glob('/Users/sahakian/SONGS/CHIRP/LaJolla/nav/LINES/*.txt')

#Now first convert to kingdom files:
for i in range(len(chirpPaths)):
    print i
    chirpNav.cnav2king(chirpPaths[i])

llPaths=glob('/Users/sahakian/SONGS/CHIRP/LaJolla/nav/LINES/kingdom/LL/*.ll')
numskip=3
for j in range(len(llPaths)):
    print j
    chirpNav.ll2utm(llPaths[j],numskip)