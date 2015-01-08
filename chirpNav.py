##~* File including all functions for handling CHIRP nav files *~##
## V.J.Sahakian 13 Nov. 2014

def cnav2king(cnavfile):
#Convert CHIRP nav files to Kingdom lat/lon, save them in a subdirectory of the 
#nav directory: /nav/kingdom/LL
#VJS 11 November 2014
#
#CHIRP format:
#   CHIRP line name   Shot?   X/Lon   Y/Lat   Time?
#Convert to:
#   Shot   X/Lon   Y/Lat
#Usage:
#   First create subdirectory /kingdom/LL 
#   cnavfile:   string with path to the chirp nav file you wish to convert
#               should end in .txt, .nav, etc. (cnavfile.txt)
#
#Output:
#   places in subdirectory /kingdom/LL,
#   named cnavfile.ll
    
    import numpy as np
    from os import path
    
    #Get main path
    cPath=path.split(cnavfile)[0]+'/'
    kingPath=cPath+'kingdom/LL/'
    #Get Line name
    line=path.split(cnavfile)[1].split(".")[0]
    #Get name of output file for kingdom
    kingLL=kingPath+line+'.ll'
    
    #Open CHIRP nav file
    chirp_dat=np.genfromtxt(cnavfile,delimiter='\t')
    shot=chirp_dat[:,1]
    lon=chirp_dat[:,2]
    lat=chirp_dat[:,3]

    #Write this to file
    king_format=np.c_[shot, lon, lat]
    np.savetxt(kingLL,king_format,fmt='%6i\t%12.8f\t%10.8f')
    
    
    
def ll2utm(LLfile,numskip):
#Convert lat/lon kingdom format files (Shot Lon Lat) to UTM
#Save in a subdirectory - /kingdom/UTM
#
#Format of kingdom file:
#   Shot   Lon   Lat
#
#Usage:
#   LLfile:         path of lat/lon kingdom file to convert
#   numskip:        number of characters to skip at the end of the path, i.e.,
#                   want them to be saved in a directory UTM at the same level 
#                   that they're in (so if they're in kingdom/LL/, want them to
#                   be in kingdom/UTM/ - so would skip 3 characters, LL/)

    import numpy as np
    import utm
    from os import path
    
    #Get main path
    llPath=path.split(LLfile)[0]+'/'
    kingPath=llPath[0:-numskip]
    #Get line name
    line=path.split(LLfile)[1].split(".")[0]
    #Get name of output file 
    utmFile=kingPath+'UTM/'+line+'.xy'
    
    #Now read in the data
    latlon=np.genfromtxt(LLfile)
    UTM=np.zeros((len(latlon),2))
    for i in range(len(latlon)):
        utmTup=utm.from_latlon(latlon[i,2],latlon[i,1])
        UTM[i,0]=utmTup[0]   #Easting (x)
        UTM[i,1]=utmTup[1]   #Northing (y)
        
    #Concatenate with shots and print out:
    utmOut=np.c_[latlon[:,0],UTM]
    np.savetxt(utmFile,utmOut,fmt='%6i\t%15.8f\t%16.8f')
    
    
def shannon2king(globfile):
#Runs by inputting a glob file of shannon's nav files to shannon2king
#Before running, make a glob file for each - then run shannon2king on teh glob
#file.  This puts them all in the dir: xys/kingdom/LL
#**Create subdirectory /kingdom/LL in the same directory as latlon.xys!!
#
#Usage:
#   globfile:   array, each entry is a path name to convert
#Output:
#   line.ll:    kingdom lat/lon file, saved in subdir kingdom/LL
#

    import numpy as np
    from os import path
    from glob import glob
    #First, turn into a kingdom file:
    for i in range(len(globfile)):
        navfile=globfile[i]
        #Pull out the chirp nav file's path, the line name, and the future kingdom 
        #file path (latlon) with the line name
        cPath=path.split(navfile)[0]+'/'
        line=path.split(navfile)[1].split(".")[0]
        kingPath=cPath[0:-11]+'kingdom/LL/'+line+'.ll'
        
        #Now pull out data:
        chirpdata=np.genfromtxt(navfile)
        shot=chirpdata[:,3]
        lon=chirpdata[:,1]
        lat=chirpdata[:,2]
        
        #Write to file
        kingformat=np.c_[shot,lon,lat]
        np.savetxt(kingPath,kingformat,fmt='%7i\t%11.6f\t%9.6f')    

    


