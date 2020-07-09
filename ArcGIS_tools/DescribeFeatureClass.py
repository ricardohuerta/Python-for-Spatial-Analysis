# -*- coding: utf-8 -*-
"""
Script: DescribeFeatureClass

Created on Sat May 16 11:22:34 2020

@author: Ricardo Huerta

Describes a feature class to identify the geometry of the feature class
"""

import arcpy

###Set workspace based on user input
ws = arcpy.GetParameterAsText(0)
arcpy.env.workspace = ws

###Get feature class from user
fc = arcpy.GetParameterAsText(1)

#Describe the feature class and assign the describe object to a variable
desc = arcpy.Describe(fc)

#Print message about checking for geometry
arcpy.AddMessage(f"Checking {fc} feature class geometry!")

#Check the geometry of the feature class and print a string
#describing the geometry.
if desc.shapeType == "Polygon" or "Point" or "Polyline":
    arcpy.AddMessage(f"{fc} feature class is a {desc.shapeType}")

else:
   arcpy.AddMessage(f"{fc} feature class has an unknown geometry type")
