# -*- coding: utf-8 -*-
"""
Script: Update Field

Created on Mon May 18 12:18:35 2020

@author: Ricardo

Adds a a text field to a field class and updates
the fields using values conctenated from two existing
fields.
"""

import arcpy

###Set workspace based on user input
ws = arcpy.GetParameterAsText(0)
arcpy.env.workspace = ws

###Get feature class from user input
fc = arcpy.GetParameterAsText(1)

#Get datasources from user input
data_source1 = arcpy.GetParameterAsText(2)
data_source2 = arcpy.GetParameterAsText(3)

#Get new field name from user input
new_fn = arcpy.GetParameterAsText(4)

#Add message to the console
arcpy.AddMessage(f"Adding field with name {new_fn}...")

#Add field to feature class
try:
    arcpy.AddField_management(fc, new_fn, "TEXT")
except:
    arcpy.GetMessages(2)

#Add message to console
arcpy.AddMessage(f"Updating {new_fn} field with values from {data_source1} and {data_source2}...")

#Create update cursor
with arcpy.da.UpdateCursor(fc, [data_source1, data_source2, new_fn]) as cursor:
    i = 0 
    for row in cursor:
        row[2] = (str(row[0]) + " " + str(row[1])).lstrip()
        cursor.updateRow(row)
        i +=1
    arcpy.AddMessage(f"{i} field(s) were updated")
