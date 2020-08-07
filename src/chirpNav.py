##~* File including all functions for handling CHIRP nav files *~##
## V.J.Sahakian 13 Nov. 2014

def cnav2king(cnavfile):
    '''
    Convert CHIRP nav files to Kingdom lat/lon, save them in a subdirectory of the 
    nav directory: /nav/kingdom/LL
    VJS 11 November 2014
    
    CHIRP format:
        CHIRP line name   Shot?   X/Lon   Y/Lat   Time?
    Convert to:
        Shot   X/Lon   Y/Lat
    Usage:
        First create subdirectory /kingdom/LL 
        cnavfile:   string with path to the chirp nav file you wish to convert
                    should end in .txt, .nav, etc. (cnavfile.txt)
        
    Output:
        places in subdirectory /kingdom/LL,
        named cnavfile.ll
    '''    
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
    '''
    Convert lat/lon kingdom format files (Shot Lon Lat) to UTM
    Save in a subdirectory - /kingdom/UTM
    
    Format of kingdom file:
        Shot   Lon   Lat
        
    Usage:
        LLfile:         path of lat/lon kingdom file to convert
        numskip:        number of characters to skip at the end of the path, i.e.,
                        want them to be saved in a directory UTM at the same level 
                        that they're in (so if they're in kingdom/LL/, want them to
                        be in kingdom/UTM/ - so would skip 3 characters, LL/)
    '''
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
    '''
    Runs by inputting a glob file of shannon's nav files to shannon2king
    Before running, make a glob file for each - then run shannon2king on teh glob
    file.  This puts them all in the dir: xys/kingdom/LL
    
    **Create subdirectory /kingdom/LL in the same directory as latlon.xys!!
    
    Usage:
        globfile:   array, each entry is a path name to convert
    Output:
        line.ll:    kingdom lat/lon file, saved in subdir kingdom/LL
    
    '''
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
        

def nmea2list(nmea_filepath):
    '''
    Open a NMEA file and put it into a list
    Input:
        nmea_filepath:      String with path to NMEA file
    Output:
        nmea_list:          List with strings of each line of the NMEA file
    '''

    ## Open the file:
    nmea_file = open(nmea_filepath)
    
    ## Read in each line, and strip the newline character, save in a list:
    nmea_lines = [line.rstrip('\n') for line in nmea_file]
    
    ## Close file:
    nmea_file.close()
    
    ## Return the list:
    return nmea_lines
    
    
def altus_splitgga_gll(nmea_list,format_list):
    '''
    Take a list of position entries from the altus, and split into
    separate lists for each type of file format.
    Input:
        nmea_list:      List with each line of an altus nma output file
        format_list:    List with the strings (e.g., '$GPGGA') for each type of
                            output to split out
    Output: 
        all_lists:      List with sub-lists, number of those equal to 
                            len(format_list), each one containing only the 
                            entries for each nmea format type.
    '''
    
    ## Make separate lists for formats:
    all_lists = []
    
    for format_i in range(len(format_list)):
        i_format_list = []
        i_format = format_list[format_i]
        
        ## Loop over lines in original list:
        for line_j in range(len(nmea_list)):
            j_line = nmea_list[line_j]
            if j_line.split(',')[0] == i_format:
                i_format_list.append(j_line)
        
        ## Append this format to the main list:
        all_lists.append(i_format_list)
        
    ## Return:
    return all_lists
        

                
def match_segy_nav(segy_stream,large_shot_nav_list,utm_zone,unitscalar):
    '''
    Take a large shot nav list, and replace a segy stream object's nav with 
    the values from the shot list
    Input:
        segy_stream:              Segy stream object, read in with obs.io.segy.core._read_segy(segypath,unpack_trace_headers=True) 
        large_shot_nav_list:      Pandas DF with nav info for the segy_stream, and all other lines, columns: shots_utcdatetime,lon,lat,elevation_km
        utm_zone:                 String with the UTM zone
        unitscalar:               Integer to use to multiply the UTM coordinates by. will be saved to 
                                    "scalar_to_be_applied_to_all_coordinates" in the EBCDIC header, so future
                                    processing should divide by this number to get the real units.
    Output:
        navcorrected_segystream:  Segy stream object with corrected nav
        shot_info:                Pandas dataframe with 
    '''        
    

    import numpy as np
    from pyproj import Proj
    import pandas as pd
    
    print('Replacing nav, using UTM zone ' + utm_zone + ', and unit scalar ' + np.str(unitscalar))
    
    ## Get the utc date values:
    utc_datetimes = large_shot_nav_list['shots_utcdatetime'].values
    
    ## Make a copy of the segy:
    navcorrected_segystream = segy_stream.copy()
    
    #Make projection object to convert lon/lats to utm:
    p = Proj(proj='utm',zone=utm_zone,ellps='WGS84')
    
    ## Make emtpy arrays to write out:
    shot = np.array([])
    lon = np.array([])
    lat = np.array([])
    elev = np.array([])
    x = np.array([])
    y = np.array([])

    ## Loop over the traces and pull out timing:
    for i_tracen in range(len(segy_stream)):
        if i_tracen % 1000 == 0:
            print('Replacing nav for trace ' +np.str(i_tracen))
            
        i_trace = segy_stream[i_tracen]
        i_shot_time = i_trace.stats['starttime']
        
        ## Get the shot number from the segy:
        i_shot = i_trace.stats.segy.trace_header['trace_sequence_number_within_line']
        
        ## Find where this time is in the larger list:
        i_navcorrect_time_ind = np.where(utc_datetimes == i_shot_time)[0]
        
        ## Get nav info from that list for this shot time:
        i_lon = large_shot_nav_list.loc[i_navcorrect_time_ind]['lon'].values[0]
        i_lat = large_shot_nav_list.loc[i_navcorrect_time_ind]['lat'].values[0]
        i_elev = large_shot_nav_list.loc[i_navcorrect_time_ind]['elevation_km'].values[0]
        
        ## Append to larger arrays:
        lon = np.append(lon,i_lon)
        lat = np.append(lat,i_lat)
        ## elevation here is in km
        elev = np.append(elev,i_elev)
        shot = np.append(shot,i_shot)
        
        #Project:
        i_x,i_y=p(i_lon,i_lat)
        
        ## Add to larger arrays:
        x = np.append(x,i_x)
        y = np.append(y,i_y)
        
        ## Get elevation scalar:
        elev_scalar = segy_stream[i_tracen].stats.segy.trace_header['scalar_to_be_applied_to_all_elevations_and_depths']
        
        ## Replace the EBCDIC header info with this - also multipy by the unit scalar, and make an integer:
        navcorrected_segystream[i_tracen].stats.segy.trace_header['source_coordinate_x'] = np.int(i_x*unitscalar)
        navcorrected_segystream[i_tracen].stats.segy.trace_header['source_coordinate_y'] = np.int(i_y*unitscalar)
        navcorrected_segystream[i_tracen].stats.segy.trace_header['group_coordinate_x'] = np.int(i_x*unitscalar)
        navcorrected_segystream[i_tracen].stats.segy.trace_header['group_coordinate_y'] = np.int(i_y*unitscalar)
        
        ## Multiply elevations by existing elevation scalar, to match the water depth etc. that exists - and first put elevation into m from km:
        navcorrected_segystream[i_tracen].stats.segy.trace_header['surface_elevation_at_source'] = np.int((i_elev*1000)*elev_scalar)
        navcorrected_segystream[i_tracen].stats.segy.trace_header['receiver_group_elevation'] = np.int((i_elev*1000)*elev_scalar)
        ## Save this unit scalar to what is applied to all coordinates, future processing should divide by this:
        navcorrected_segystream[i_tracen].stats.segy.trace_header['scalar_to_be_applied_to_all_coordinates'] = unitscalar
        
        ## Also make the units meters:
        navcorrected_segystream[i_tracen].stats.segy.trace_header['coordinate_units'] = 1 # 1 is used for meters and feet, 2 for arcseconds

    ## Make a list of the nav info to return:
    shot_info_dict = {'shot':shot, 'lon':lon, 'lat':lat, 'elevation':elev, 'utm_x':x, 'utm_y':y}
    shot_info = pd.DataFrame(shot_info_dict)
    
    ## Return the segystream, and also the list of corrected info:
    return navcorrected_segystream, shot_info
    
    
    
    
def create_text_header(lines):
    """Format textual header
    Create a "correct" SEG-Y textual header.  Every line will be prefixed with
    C##, are each 80 bytes long total, and there are 40 lines. 
    The input must be a dictionary with the line
    number[1-40] as a key. The value for each key should be up to 76 character
    long string.
    Parameters
    ----------
    lines : dict
        `lines` dictionary with fields:
        - ``no`` : line number (`int`)
        - ``line`` : line (`str`)
    Returns
    -------
    text : str
    """

    rows = []
    for line_no in range(1, 41):
        line = ""
        if line_no in lines:
            line = lines[line_no]
        row = "C{0:>2} {1:76}".format(line_no, line)
        rows.append(row)

    rows = ''.join(rows)
    return rows
