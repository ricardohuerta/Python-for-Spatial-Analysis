# -*- coding: utf-8 -*-

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("ImageAnalyst")

import sys
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "WiFi_AP_Model"
        self.alias = "WiFi_AP_Model"

        # List of tool classes associated with this toolbox
        self.tools = [ElevationRasterPrep, PointFeatureToAccessPointRadius]


class ElevationRasterPrep(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Elevation Raster Preparation"
        self.description = """Creates a buffer of 0 value cells around 
        point features in an elevation raster. This helps mitigate viewshed errors if the
        point features are slightly offset from their corresponding elevation points in an elevation raster"""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        ## Parameter to define output geodatabase  
        param0 = arcpy.Parameter(
            displayName="Output Workspace/Geodatabase",
            name="Workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        
        ## Autofill curretn workspace
        param0.defaultEnvironmentName = 'workspace'

        ## Parameter to define input point feature class
        param1 = arcpy.Parameter(
            displayName="Point Feature Class",
            name="APpoints",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        
        ## Limito to point features
        param1.filter.list = ["POINT"]

        ## Checkbox parameter to evaluate wether the tool will need to create a feature height raster or if the user will supply it
        param2 = arcpy.Parameter(
            displayName = "Create Feature Height Raster",
            name = "Feature Height Checkbox",
            datatype = "GPBoolean",
            parameterType= "Optional",
            direction = "Input")

        ## Parameter to define the highest hit input raster (if the user checks the chekcbox in parameter 2)
        param3 = arcpy.Parameter(
            displayName = "Highest Hit Raster",
            name = "HHraster",
            datatype= "DERasterDataset",
            parameterType="Optional",
            direction = "Input")      

        ## Parameter to define the bare earth input raster (if the user checks the checkbox in parameter 2)
        param4 = arcpy.Parameter(
            displayName= "Bare Earth Raster",
            name= "BEraster",
            datatype= "DERasterDataset",
            parameterType= "Optional",
            direction = "Input")
        
        ## Parameter to define the feature height input raster (if the user does not check the checkbox in parameter 2)
        param5 = arcpy.Parameter(
            displayName = "Feature Height Raster",
            name= "FeatureHeightRaster",
            datatype= "DERasterDataset",
            parameterType= "Optional",
            direction = "Input")
        
        ## Parameter to define the distance by which the point features will be buffered to account for point/raster offset
        param6 = arcpy.Parameter(
            displayName=  "Buffer Distance",
            name= "BufferDistance",
            datatype= "GPDouble",
            parameterType= "Required",
            direction = "Input")
        
        ## Auto fill the buffer distance to 8
        param6.value = 8

       ## Parameter to define the units fo rthe buffer distance in parameter 6
        param7 = arcpy.Parameter(
            displayName = "Buffer Distance Linear Units",
            name = "BufferDistanceLinearUnits",
            datatype =  "GPString",
            parameterType = "Required",
            direction = "Input")
        
        ## Autofill with "Feet"
        param7.value = "Feet"

        ## Limit list choices to "Feet" or "Meters"
        param7.filter.type = "ValueList"
        param7.filter.list = ["Feet", "Meters"]

        ## Parameter to define rge output feature name
        param8 = arcpy.Parameter(
            displayName= "Output Name",
            name = "OutpuName",
            datatype = "GPString",
            parameterType= "Required",
            direction= "Input")
        

        return [param0, param1, param2, param3, param4, param5, param6, param7, param8]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
        ## If checkbox parameter is checked, enable bare earth and highest hit input parameters and disable the feature height parameter
        if parameters[2].value:
            parameters[5].enabled = False            
            parameters[3].enabled = True           
            parameters[4].enabled = True
           
        ## Else (if checbox is not checked), enable the feature hieght raster parameters and disable the bare earth and highest hit raster
        ## input parameters
        else:
            parameters[5].enabled = True
            parameters[3].enabled = False 
            parameters[4].enabled = False        

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        
        ## If the checkbox is checked and highest hit and bare earth input raster parameters are not filled,
        ## Set error messages
        if parameters[2].value and not parameters[3].value and not parameters[4].value:
            parameters[3].setErrorMessage("You must supply a bare earth raster.")
            parameters[4].setErrorMessage("You must supply a highest hit raster.")

        ## Else if the checkbox is not checked and the feature height input raster parameter is not filled,
        ## Set error message
        elif not parameters[2].value and not parameters[5].value:
            parameters[5].setErrorMessage("You must supply a height raster.")

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        ## Workspace based on user input
        ws = parameters[0].valueAsText
        arcpy.env.workspace = ws
        arcpy.env.overwriteOutput = True

        ## Get point feature class from user
        input_points = parameters[1].valueAsText

        ## If the "Create Feature Height Raster" check box was checked get highest hit and bare earth rasters from user
        if parameters[2].value:
            hh_raster = parameters[3].valueAsText
            be_raster = parameters[4].valueAsText
        
        ## If the checkbox is not checked get the feature height raster from user
        else:
            height_raster = parameters[5].valueAsText
        
        ## Get the buffer distance from user
        buffer_distance = parameters[6].valueAsText

        ## Get the buffer distance units from user
        buffer_distance_units = parameters[7].valueAsText

        ## Concatenate the buffer distance with the units to create a string representation of the distance and units
        buffer_distance_string = str(buffer_distance) + ' ' + str(buffer_distance_units)

        ## Get output raster feature name from user
        out_name = parameters[8].valueAsText


        ## If the "Create Feature Height Raster" checkbox is checked create the height_raster
        if parameters[2].value:
            height_raster = hh_raster - be_raster
        
        ## Buffer point feature by user defined distance
        out_buffer = os.path.join(arcpy.env.workspace, (input_points + "Buffer"))
        arcpy.analysis.Buffer(in_features= input_points, out_feature_class= out_buffer, buffer_distance_or_field= buffer_distance_string, 
        line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

        ## Extract by mask to get raster representation of buffers
        raster_buffers = os.path.join(arcpy.env.workspace, (out_buffer + "Raster"))
        raster_buffers = ExtractByMask(height_raster, out_buffer)
        
        ## Set buffer values to zero
        zeroed_buffers = raster_buffers * 0

        ## Multiply zeroed_buffers by height_raster to get zeroaed areas around points
        final_height_raster = Con(IsNull(zeroed_buffers), height_raster, zeroed_buffers)

        ## Set local variable
        output_filepath = os.path.join(arcpy.env.workspace, out_name)
        
        ## Save output
        final_height_raster.save(output_filepath)

        return

class PointFeatureToAccessPointRadius(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Access Point Placement to Signal Strength Field"
        self.description = '''Takes a point feature class representing potential wifi access point locations 
        and outputs raster features for each point representing wifi signal strength'''
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        ## Parameter to define the workspace/geodatabse where output will be written
        param0 = arcpy.Parameter(
            displayName="Output Workspace/Geodatabase",
            name="Workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        
        ## Autofill to curretn workspace
        param0.defaultEnvironmentName = 'workspace'
        
        ## Paramter to define the input point features
        param1 = arcpy.Parameter(
            displayName="Point Feature Class",
            name="APpoints",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        
        ## Limit feature types to points
        param1.filter.list = ["POINT"]

        ## Parameter to define the prefix that will be prepended to the output rasters
        param2 = arcpy.Parameter(
            displayName="Output Feature Class Prefix",
            name="OutputFC",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
        ## Parameter to define the field that will be used to ID the output rasters. The values from this field will be appended to
        ## the ouput rasters
        param3 = arcpy.Parameter(
            displayName="Unique ID Field",
            name="Unique ID",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        
        ## Limit field types for this parameter to text fields
        param3.filter.list = ['Text']

        ## Set dependencies for this parameter to the point feature set defined in parameter 1
        param3.parameterDependencies = [param1.name]

        ## Parameter to define the feature elevation input raster 
        param4 = arcpy.Parameter(
            displayName= "Elevation Raster", 
            name= 'elevRaster',
            datatype = "DERasterDataset",
            parameterType= 'Required',
            direction= 'Input')

        ## Parameter to define the height of access point placement
        param5 = arcpy.Parameter(
            displayName = 'Acess Point Height in Meters',
            name = 'APheight',
            datatype= "GPDouble",
            parameterType = "Required",
            direction="Input")
        
        ## Parameter to define the viewshed radius value
        param6 = arcpy.Parameter(
            displayName = "Viewshed Radius in Meters",
            name= "ViewRadius",
            datatype = "GPDouble",
            parameterType = "Required",
            direction = "Input")
        
        ## Auto fill to 91.44 meters
        param6.value = 91.44

        ## Parameter to define the access point broadcast frequency 
        param7 = arcpy.Parameter(
            displayName = "Access Point Broadcast Frequency in MHz",
            name = "BroadcastFrequency",
            datatype = "GPLong",
            parameterType = "Required",
            direction = "Input")
        
        ## Autofill to 2400
        param7.value = 2400

        ## Parameter to define access point transmit power 
        param8 = arcpy.Parameter(
            displayName = "Access Point Transmit Power in dBm",
            name = "TransmitPower",
            datatype = "GPDouble",
            parameterType = "Required",
            direction = "Input")

        ## Autofill to 20
        param8.value = 20

        return [param0, param1, param2,  param3, param4, param5, param6, param7, param8]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        ## Workspace based on user input
        ws = parameters[0].valueAsText
        arcpy.env.workspace = ws
        arcpy.env.overwriteOutput = True

        ## Get point FC from user 
        AP_points = parameters[1].valueAsText

        ## Get output FC prefix from user
        out_name = parameters[2].valueAsText

        ## Get field that contains the cartegraph ID of lampposts from user
        ID_field = parameters[3].valueAsText

        ## Get elevation raster from user
        elev_raster = parameters[4].valueAsText

        ## Get access point height from user
        AP_height = parameters[5].valueAsText

        ## Get outer radius value for viewshed tool from user
        outer_radius = parameters[6].valueAsText

        ## Get frequency value from user  
        FREQUENCY = float(parameters[7].valueAsText)

        ## Get transmit power value fron user
        TRANSMIT_POWER = float(parameters[8].valueAsText)
        
    
        # Set processing extent
        arcpy.env.extent = elev_raster

        ## 1. Get the viewshed at 300ft radius (91.44 meters)
        ## in: point light feature, polygon park feature
        ## out: polygon feature reprsenting visible areas of the park fpr each point

        # Initiate search cursor
        with arcpy.da.SearchCursor(AP_points, ID_field) as cursor:
            # Iterate through cursor and make a selection where ID_field = the current row
            for row in cursor:
                # Clean unique field of invalid string characters
                clean_row = row[0].replace('-','')

                # Define the name of the output viewshed feature
                out_vs_fc = f'{out_name}_viewshed_{clean_row}'
                
                # Define the name of the output field of view feature
                out_fov_fc = f'{out_name}_fov_{clean_row}'
                
                # Define the name of the range radius feature
                out_range_radius_feature_class = f'{out_name}_range_radius_{clean_row}'
                
                arcpy.AddMessage(f'creating field of view for lightpost with Carte ID {row[0]}...')
                
                # Run the radial line of sight tool
                arcpy.RadialLineOfSightAndRange_defense(arcpy.management.SelectLayerByAttribute(AP_points, 
                                                                                                selection_type = 'NEW_SELECTION',
                                                                                                where_clause = f"{ID_field} = '{row[0]}'"), 
                                                        elev_raster, out_vs_fc, out_fov_fc, out_range_radius_feature_class,
                                                        AP_height, 0, outer_radius)

                
            ## 2. Calculate distance raster with the Euclidean distance tool
            ## Make sure to set processing extent to limits of park polygon in the environment
                
                # Print message to the console
                arcpy.AddMessage('Calculating distance raster...')
                
                # Set local variables
                inSourceData = arcpy.SelectLayerByAttribute_management(AP_points, "NEW_SELECTION", f"{ID_field} = '{row[0]}'")
                
                # Execute euclidean distance tool
                outEucDistance = EucDistance(inSourceData)

            ## 3. Convert the distance values from native linear unit to km in the raster calculator
            ## km = feet * 0.0003048
                                    
                # Get linear units from euclidean distance raster derived from input raster
                spatial_ref = arcpy.Describe(outEucDistance).spatialReference
                M_PER_UNIT = spatial_ref.metersPerUnit

                # Execute raster algebra to covert feet to km
                outEucDistanceM = outEucDistance * M_PER_UNIT
                
            ## 4. Calculate free space path loss (FSPL) in raster calculator
            ## FSPL = 20log10(d) + 20 log10(f) + -27.55 'https://www.hindawi.com/journals/complexity/2018/7560717/#EEq2'
            ## d is distance in m and f is frequency of wifi signal in MHz (commonly 2400)
            ## FSPL is output in db
                
                # Print message to the console
                arcpy.AddMessage('Calculating free space path loss...')

                # Execute raster algebra
                outFSPL = TRANSMIT_POWER *  Log10(outEucDistanceM) + 20 * Log10(FREQUENCY) + -27.55
                    
            ## 5. Convert viewshed polygon to raster with Polygon to Raster tool
                
                # Print message to the console
                arcpy.AddMessage('Converting viewshed polygon to raster...')

                # Set local variable
                in_polygon = f'{out_name}_viewshed_{clean_row}'
                output_raster = f'viewshed_{clean_row}_raster'

                # Execute raster conversion
                arcpy.conversion.PolygonToRaster(in_polygon, 'VISIBILITY', output_raster)

            ## 6. Reclassify viewshed raster so that visible cells have a value of 0 and non-visible cells have a value of 1
                
                # Set local variables
                in_raster = f'viewshed_{clean_row}_raster'
                
                reclass_field = 'Value'
                remap = RemapValue([[1,0], [0,1]])

                # Execute reclassify
                outReclass = Reclassify(in_raster, reclass_field, remap)
                
            ## 7. Calculate the loss signal at every cell using an average signal attenuation cause by tree (5.6 dB) 
            ## 'City Trees and Municipal Wi-Fi Networks: Compatibility of Conflict' Igor Lacan, Joe R. McBride
            ## loss signal = reclassifed viewshed * 5.6 (Assuming the only things obstructing viewshed are trees)
            ## Alternatively could classify aerial imagery to identify different classes of obstacles and calculate signal 
            ## attenuation according to material   
                
                # Print message to the console
                arcpy.AddMessage('Calculating signal attenuation from trees...')

                # Set local variable    
                TREE_ATTENUATION = 5.6

                # Execute raster calculator
                loss_signal = outReclass * TREE_ATTENUATION
                                        
            ## 8. Calculate received power at every cell 
            ## emitted power modelled at 100mW = 20dbm
            ## received power = tranmitted power - (FSPL - L0)     
                
                # Set local variable
                output_filepath = os.path.join(arcpy.env.workspace, f'Prx_{clean_row}')

                # Execute raster calculator
                received_power = 20 - (outFSPL + loss_signal) 
                
                # Save output
                received_power.save(output_filepath)

        ## Clear selection
        arcpy.management.SelectLayerByAttribute(AP_points, selection_type = 'CLEAR_SELECTION')
                                                                                                             
        
