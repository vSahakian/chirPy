#Convert Shannon's xys files to Kingdom format
#VJS 13 Nov 2014
#
#Format is usually:
#   File_name   lon   lat   shot  
#The files are contained in the directory/subdirectories:
#   xys_files/xys/latlon.xys
#Naming convention:
#   line_number.*latlon.xys

import numpy as np
from os import path
from glob import glob
import chirpNav
#
#Runs by inputting a glob file of shannon's nav files to shannon2king
#Before running, make a glob file for each - then run shannon2king on teh glob
#file.  This puts them all in the dir: xys/kingdom/LL
    
s2013p=glob('/Users/sahakian/SONGS/CHIRP/2013survey/xys_files/xys/latlon.xys/*latlon.xys')
s2009p=glob('/Users/sahakian/SONGS/CHIRP/sproul_09/xys_files/xys/xys/latlon.xys/*latlon.xys')
s2008p=glob('/Users/sahakian/SONGS/CHIRP/sproul_08/xys_files/xys/xys/latlon.xys/*latlon.xys')

#Convert to kingdom files for each survey
chirpNav.shannon2king(s2013p)
chirpNav.shannon2king(s2009p)
chirpNav.shannon2king(s2008p)

#Set numskip to 3, so it will put them into kingdom/UTM
numskip=3

#Define the lat lon glob file for each survey
s2013ll=glob('/Users/sahakian/SONGS/CHIRP/2013survey/xys_files/xys/kingdom/LL/*.ll')
s2009ll=glob('/Users/sahakian/SONGS/CHIRP/sproul_09/xys_files/xys/xys/kingdom/LL/*.ll')
s2008ll=glob('/Users/sahakian/SONGS/CHIRP/sproul_08/xys_files/xys/xys/kingdom/LL/*.ll')

#Now convert all to utm and save them in xys/kingdom/UTM:
for j in range(len(s2013ll)):
    print j
    chirpNav.ll2utm(s2013ll[j],numskip)

for k in range(len(s2009ll)):
    print k
    chirpNav.ll2utm(s2009ll[k],numskip)
    
for l in range(len(s2008ll)):
    print l
    chirpNav.ll2utm(s2008ll[l],numskip)
    

    
    
    
