# -*- coding: utf-8 -*-
"""
Created on Thu May  7 23:08:11 2020

@author: chmar
"""




# Import necessary libraries
from datetime import datetime, timedelta
import os
# Change working directory

#take the start and end date from the namelist
from namelist_geos_scripts import storm_folder, GEOS_start, GEOS_end, path_to_storm, path_to_geos2wps, iLonMin, iLonMax, jLatMin, jLatMax
os.chdir(path_to_storm)
start = GEOS_start
end= GEOS_end


#%% 
# The outfolder for this field was created by the download_wrapper
out_folder = storm_folder + '/U'
# Go inside the out folder
os.chdir(out_folder)
#go through and iterate each variable over every time step, by creating a namelist for each timestep and running geos2wps 
ls_command='ln -s ' + path_to_geos2wps
os.system(ls_command)

#first, see if the files you need are there
now=start
while now<= end:
    filename = 'c1440_NR' +'.' 'inst30mn_3d_U_Nv' +'.' + now.strftime('%Y%m%d_%H%Mz') + '.' +'nc4'
    folder = 'https://g5nr.nccs.nasa.gov/data/DATA/0.0625_deg/inst/'
    data_field = 'inst30mn_3d_U_Nv'
    url = folder + data_field # folder where data is kept
    url = url + now.strftime('/Y%Y/M%m/D%d/') # specific date
    url = url + 'c1440_NR.'
    url = url + data_field 
    url = url + now.strftime('.%Y%m%d_%H%Mz')
    url = url + ".nc4"
    command="wget --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t" + url
    
    if not os.path.exists(filename):
        os.system(command)
    now += timedelta(0, 30*60)
now = start
#create a namelist
while now <= end:
   namelist=open('namelist.geos2wps', 'w') 
   filename = 'c1440_NR' +'.' 'inst30mn_3d_U_Nv' +'.' + now.strftime('%Y%m%d_%H%Mz') + '.' +'nc4'
   timestamp=now.strftime('%Y-%m-%d_%H:%M') 
   namelist.write("&files\n")
   namelist.write("\n")
   namelist.write("geosFileFormat=2,\n")
   namelist.write("geosFileName=" +repr(filename)+ ",\n" )
   namelist.write("outputDirectory='./',\n")
   namelist.write("/\n")
   namelist.write("\n")
   namelist.write("&coordinates\n")
   namelist.write("longitudeName='lon',\n")
   namelist.write("latitudeName='lat',\n")
   namelist.write("hasVerticalDimension=.true.,\n")
   namelist.write("verticalName='lev',\n")
   namelist.write("/\n")
   namelist.write("&forecast\n")
   namelist.write("numberOfTimes=1,\n")
   namelist.write("validTimes(1)=" + repr(timestamp)+",\n")
   namelist.write("timeIndices(1)= 1, \n")
   namelist.write("forecastHours(1)= 0, \n")
   namelist.write("/\n")
   namelist.write("\n")
   namelist.write("&variables\n")
   namelist.write("numberofVariables=1\n")
   namelist.write("\n")
   namelist.write("variableRanks(1) = 4,\n") 
   namelist.write("variableLevelTypes(1) = 11,\n") 
   namelist.write("variableNamesIn(1)='U',\n") 
   namelist.write("variableNamesOut(1)='UU',\n") 
   namelist.write("variableUnits(1)='m s-1',\n") 
   namelist.write("variableDescriptions(1)='eastward wind',\n") 
   namelist.write("\n")
   namelist.write("/\n")
   namelist.write("&subsetData\n")
   namelist.write("subset=.true.,\n")
   namelist.write("iLonMin=" + str(iLonMin) + ",\n") 
   namelist.write("iLonMax=" + str(iLonMax) + ",\n") 
   namelist.write("jLatMin=" + str(jLatMin) + ",\n") 
   namelist.write("jLatMax=" + str(jLatMax) + ",\n")
   namelist.write("kVertMin=1,\n") 
   namelist.write("kVertMax=72,\n")
   namelist.write("/")
   namelist.close()
   namelist=open("namelist.geos2wps", "r")
   print(namelist)
   test=namelist.read()
   print(test)
   namelist.close() 
   #now run geos2wps
   command = 'srun ./geos2wps'
   os.system(command)

   #move on to the next timestep
   now += timedelta(0, 30*60)
   
