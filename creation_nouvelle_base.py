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
zak = genfromtxt('medchl.csv', delimiter=',')


err_cloud=0.02
err_invalide=0.02
err_land=0.02

a=[]
for i in range(len(zak[:,1])-1):
    if ((zak[i+1,3]<=err_cloud)  & (zak[i+1,4]<=err_invalide)& (zak[i+1,5]<=err_land)):
        a.append(i)

keep = np.zeros(shape=ds.dims['index']).astype(bool)
keep[[a]] = True
chlanew = ds.chla[keep]
chlanew.shape


flagnew = ds.flags[keep]
ds_new = xr.Dataset({'chla':chlanew,'flags':flagnew})
ds_new.to_netcdf('../data/nouvellebase.nc')


