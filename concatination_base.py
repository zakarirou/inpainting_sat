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

from sklearn.preprocessing import Imputer
imp = Imputer(strategy="mean")


ds = xr.open_dataset('../data/medchl.nc')
data = genfromtxt('medchl.csv', delimiter=',')


err_cloud=0.05
err_invalide=0.05
err_land=0.05

a=[]
for i in range(len(data[:,1])-1):
    if ((data[i+1,3]<=err_cloud)  & (data[i+1,4]<=err_invalide)& (data[i+1,5]<=err_land)):
        a.append(i)

keep = np.zeros(shape=ds.dims['index']).astype(bool)
keep[[a]] = True

chlanew = ds.chla[keep]
flagnew= ds.flags[keep]




dsss = xr.Dataset({'chla':chlanew,'flags':flagnew})
nan_locs = np.where(np.isnan(dsss.chla[3,:,:]))
np.shape(nan_locs)
ds_new = xr.Dataset({'chla':chlanew,'flags':flagnew})
for i in range (len(flagnew)):
    ds_new.chla[i,:,:] = imp.fit_transform(ds_new.chla[i,:,:])

ds1=xr.Dataset({'chla':chlanew,'flags':flagnew})
ds1.index.values= ds1.index.values +1000000
for i in range (len(flagnew)):
    ds1.chla[i,:,:] = imp.fit_transform(ds1.chla[i,:,:])
ds2=xr.Dataset({'chla':chlanew,'flags':flagnew})
ds2.index.values= ds2.index.values +2000000
for i in range (len(flagnew)):
    ds2.chla[i,:,:] = imp.fit_transform(ds2.chla[i,:,:])
ds3=xr.Dataset({'chla':chlanew,'flags':flagnew})
ds3.index.values= ds3.index.values +3000000
for i in range (len(flagnew)):
    ds2.chla[i,:,:] = imp.fit_transform(ds2.chla[i,:,:])
ds4=xr.Dataset({'chla':chlanew,'flags':flagnew})
ds4.index.values= ds4.index.values +4000000
for i in range (len(flagnew)):
    ds4.chla[i,:,:] = imp.fit_transform(ds4.chla[i,:,:])

dds=xr.concat([ds_new, ds1,ds2,ds3,ds4], 'index')
dds.to_netcdf('../data/essaaybase.nc')
dds