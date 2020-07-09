# -*- coding: utf-8 -*-
"""
Script: Check if Feature Class Exists

Created on Sat May 16 10:17:39 2020

@author: Ricardo

This Script checks if a feature class exists. 
If the feature class exists, it deletes that class.
If the feature class does not exist, 
it creates that class
"""


import arcpy


###Set workspace based on user input
ws = arcpy.GetParameterAsText(0)
arcpy.env.workspace = ws

###Get feature class from user
fc = arcpy.GetParameterAsText(1)


#Display information about script running
arcpy.AddMessage(f"Checking if {fc} exists...")

#Check if feature class exists
if arcpy.Exists(fc):
    #Display information about feature class deletion
    arcpy.AddMessage(f"{fc} exists, deleting...")
    #Delete feature class if it exists
    arcpy.Delete_management(fc)
    #Display information about script copmletion
    arcpy.AddMessage(f"{fc} deleted")
    
#If the feature class does not exist, create the 
#feature class
else:
    #Display information about feature class creation
    arcpy.AddMessage(f"{fc} does not exist!"
                     f"Creating {fc}...")
    arcpy.CreateFeatureclass_management(arcpy.env.workspace, fc)  
    #Display information about feature class creation
    arcpy.AddMessage(f"{fc} created")
    


