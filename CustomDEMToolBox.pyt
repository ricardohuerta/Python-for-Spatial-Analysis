import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "DEM_Modeling"
        self.alias = "DEM_Modeling"

        # List of tool classes associated with this toolbox
        self.tools = [PolylineToElevationPoints]


class PolylineToElevationPoints(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Polyline To Elevation Points"
        self.description = "Takes a polyline feature class with elevation data for the endpoints as input and outputs a point feature class with downward trending z-values for each feature." 
        self.canRunInBackground = False


    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Output Workspace/Geodatabase",
            name="Workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Polyline Feature Class",
            name="PolylineFC",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param1.filter.list = ["Polyline"]

        param2 = arcpy.Parameter(
            displayName="Output Feature Class",
            name="OutputFC",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param3 = arcpy.Parameter(
            displayName="Upstream Elevation Field",
            name="USelev_field",
            datatype="Field",
            parameterType="Optional",
            direction="Input")
        #param3.value = "USelev"
        param3.filter.list = ['Double', 'Long', 'Float', 'Short']
        param3.parameterDependencies = [param1.name]


        param4 = arcpy.Parameter(
            displayName="Downstream Elevation Field",
            name="DSelev_field",
            datatype="Field",
            parameterType="Optional",
            direction="Input")
        #param4.value = "Dselev"
        param4.filter.list = ['Double', 'Long', 'Float', 'Short']
        param4.parameterDependencies = [param1.name]

        param5 = arcpy.Parameter(
            displayName="Point Spacing (meters)",
            name="PointSpacingMeters",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")

        return [param0, param1, param2, param3, param4, param5]


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
        ### Workspace based on user input
        ws = parameters[0].valueAsText
        arcpy.env.workspace = ws
        arcpy.env.overwriteOutput = True

        ### Get polyline fc from user
        polyline = parameters[1].valueAsText

        ### Get output fc name
        outputFC = parameters[2].valueAsText

        ### Get US and DS elevation fields
        USelev = parameters[3].valueAsText
        DSelev = parameters[4].valueAsText

        ### Get point spacing value in meters
        pointSpacing = parameters[5].valueAsText



        ### Create point feature class from points for each objectID
        arcpy.GeneratePointsAlongLines_management(polyline, outputFC, 'DISTANCE', Distance = float(pointSpacing),
                                                  Include_End_Points='END_POINTS')

        ### Add field to store z-values in
        arcpy.AddField_management(outputFC, 'z_value', 'FLOAT')

        ### Get unique Object ID's from original polyline fc
        ORIG_FID_LIST = self.unique_values(polyline, 'OBJECTID')

        ### Calculate slope and z-values for point feature class
        for FID in ORIG_FID_LIST:
            slopeCalculated = False
            where_clause = "ORIG_FID = {FID}".format(FID = FID)
            counter = 0
            featureCount = len(
                list(i for i in arcpy.da.SearchCursor(outputFC, ['OBJECTID'], where_clause=where_clause)))

            with arcpy.da.UpdateCursor(outputFC, [USelev, DSelev, 'z_value'], where_clause=where_clause) as cursor:
                for row in cursor:
                    while slopeCalculated == False:
                        slope = self.calculateSlope(float(row[0]), float(row[1]), featureCount)
                        slopeCalculated = True

                    if row[0] > row[1]:
                        row[2] = float(row[0]) - float(slope * counter)
                        counter += 1
                        cursor.updateRow(row)

                    elif row[1] > row[0]:
                        row[2] = float(row[1]) - float(slope * counter)
                        counter += 1
                        cursor.updateRow(row)
                        
                        
    # Define function to get unique values from a cursor
    def unique_values(self, table, field):
        with arcpy.da.SearchCursor(table, [field]) as cursor:
            return sorted([row[0] for row in cursor])
            
    # Define a function to calculate the slope between two polyline endpoints
    def calculateSlope(self, elev1, elev2, featureCount):
            absolute = float(abs(elev1 - elev2))
            slope = absolute / float(featureCount)
            return slope
    

    # End do_analysis function




