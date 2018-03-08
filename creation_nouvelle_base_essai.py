# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 15:56:55 2018

pour faire une nouvelle base en jouant sur le pourcentage des valeurs manquantes 

err_cloud
err_invalide
err_land

@author: DELL
"""
import numpy as np
import xarray as xr
from numpy import genfromtxt

ds = xr.open_dataset('../data/medchl.nc')
data = genfromtxt('medchl.csv', delimiter=',')


err_cloud=0.05
err_invalide=0.05
err_land=0.05
pourcentage_apprentissage = 0.7
a=[]
for i in range(len(data[:,1])-1):
    if ((data[i+1,3]<=err_cloud)  & (data[i+1,4]<=err_invalide)& (data[i+1,5]<=err_land)):
        a.append(i)

keep_app = np.zeros(shape=ds.dims['index']).astype(bool)
keep_val = np.zeros(shape=ds.dims['index']).astype(bool)
app=int(np.floor(len(a)-1) *pourcentage_apprentissage )

a1=a[0: app]
a2=a[(app+1) :]
a2
keep_app[[a1]] = True
keep_val[[a2]] = True


chlanew_app = ds.chla[keep_app]
flagnew_app = ds.flags[keep_app]

chlanew_val = ds.chla[keep_val]
flagnew_val = ds.flags[keep_val]

ds_new1 = xr.Dataset({'chla':chlanew_app,'flags':flagnew_app})
ds_new1.to_netcdf('../data/base_apprentissage.nc')

ds_new2 = xr.Dataset({'chla':chlanew_val,'flags':flagnew_val})
ds_new2.to_netcdf('../data/base_validation.nc')

