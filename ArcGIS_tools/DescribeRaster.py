# -*- coding: utf-8 -*-
"""
Script: Describe Raster

Created on Mon May 18 10:13:13 2020

@author: Ricardo Huerta

Describes a raster to get the extent of the raster
"""

import arcpy

#Get raster file from user input
raster = arcpy.GetParameterAsText(0)


#Describe raster dataset
desc = arcpy.Describe(raster)

#Print message to the menu
arcpy.AddMessage(f"Describing raster located at {desc.catalogPath}")

#Call and print the extent attribute
extent = desc.extent
arcpy.AddMessage(extent)

#Print data type for the raster
if desc.IsInteger == True:
    arcpy.AddMessage(f"{desc.baseName} is an integer type!")

elif desc.IsFloat == True:
   arcpy.AddMessage(f"{desc.baseName} is a float type!")

else:
    arcpy.AddMessage(f"{desc.baseName} is an unknown type!")

