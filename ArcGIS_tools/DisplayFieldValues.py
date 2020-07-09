# -*- coding: utf-8 -*-
"""
Script: Display Field Values

Created on Mon May 18 11:33:52 2020

@author: Ricardo Huerta

Displays field values for a selected field of an input feature class
"""
import arcpy

#Get feature class from user input
fc = arcpy.GetParameterAsText(0)

#Get field name from user input
fn = arcpy.GetParameterAsText(1)

#Print message to the console about running script
arcpy.AddMessage(f"Searching {fn} field in the feature class located at {fc}...")

#Create search cursor for user defined feature class and field name
with arcpy.da.SearchCursor(fc, [fn]) as cursor:
    
    #Create counter variable and set to 0
    i = 0
    
    #Loop through the cursor and print out the rows and number of rows
    for row in cursor:
        arcpy.AddMessage(f"Value: {str(row)}")
        i += 1
    arcpy.AddMessage(f"There are {i} rows in the {fn} field!")
       
       
       
       


