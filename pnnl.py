"""

NOTE: Include this code in a new folder with the required datasets.

Had a trouble downloading the netcdf files directly from the link 
from the runtime and it didn't work. Otherwise would be automated. 
Hope that's fine.

"""
from netCDF4 import Dataset
import numpy as np
import os
import glob

os.chdir('C:\\Users\\rayud\\Desktop\\Python\\ass')
mylist = glob.glob('sgpmetE13.b1.2018100*.cdf')


for fName in mylist: # Starting the loop for each file
    nc = Dataset(fName,'r',format = 'NETCDF4') # Read the file
    temp = nc.variables['temp_mean'][:] # Extract temp_mean
    press = nc.variables['atmos_pressure'][:] # Extract atmos_pressure
    t = nc.variables['time'][:] # Extracting time in Seconds
    time = t/60 # Converting time to minutes
    nc.close() # Done extracting values from the input file
    temp_sum = 0 # Variable Initilization
    press_sum = 0
    i = 0; j = 0; k = 0
    temp_avg = np.zeros(int(len(time)/5),dtype = 'f') #Creating 1D arrays
    press_avg = np.zeros(int(len(time)/5),dtype = 'f')
    time_avg = np.zeros(int(len(time)/5),dtype = 'f')
    # For 5 min averaged temperature and pressure:
    for i in range(len(time)): # Interior loop to compute 5 min averages
        temp_sum += temp[i]
        press_sum += press[i]
        j +=1 # j increases by 1 for each minute
        if(j == 5): # 5 min average starts here
            j = 0
            temp_avg[k] = temp_sum/5 # Computes the average here
            press_avg[k] = press_sum/5
            time_avg[k] = i+1 #Stores value of 5 min interval
            k +=1 # k increases by 1 for every 5 minutes
            temp_sum = 0 # Sets the 5 min sum to 0
            press_sum = 0
    
    # Creating a new output file begins here:
    fName_new = 'sgpmetavg' + fName[6:] # Required output file name
    new_nc = Dataset(fName_new,'w') # Creating netcdf file
    
    # Dimensions    
    new_time = new_nc.createDimension('Time',k)
#    t_mean = new_nc.createDimension('Temperature',k)
#    p_mean = new_nc.createDimension('Pressuere',k)
    
    
    # Global Attributes
    new_nc.source = os.getcwd()
    new_nc.title = 'Temperature and Atmospheric Pressure values for Southern Great Plains, Lamont, Oklahoma'
    new_nc.references = 'ftp://ftp.arm.gov/pub/users/sivaraman/candidates-projects/DATA/'
    new_nc.interval = 'Averaged for 5 minutes'
    new_nc.history = 'Created using python at 11/14/18'
    
    # Variables
    times = new_nc.createVariable('time',np.int32,('Time',))
    temps = new_nc.createVariable('mean_temperature',np.float32,('Time',))
    pressure = new_nc.createVariable('atmospheric_pressure',np.float32,('Time',))
    
    # Variable Attributes
    times.units = 'minutes'
    times.long_name = 'Time offset from midnight'
    temps.units = 'degC'
    temps.long_name = 'Mean Temperature'
    temps.missing_value = -9999
    pressure.units = 'kPa'
    pressure.long_name = 'Atmospheric Pressure'
    pressure.missing_value = -9999
    
    # Writing Data
    
    times[:] = time_avg
    pressure[:] = press_avg
    temps[:] = temp_avg
    new_nc.close()

print("Run Successfull!")
print(os.listdir())



    
    
    