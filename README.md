# Spatial Analysis Tools in Python
I will use this repository to track my forays in to spatial analysis using python.

## Arc GIS Pro Tools
These are simple tools i created to perform common aptial analysis and manipulation tasks for Arc GIS Pro. 
 
## Social Vulnerability Analysis
This is a social vulnerability analysis for county census tracts in the Portland Metro Statistical Area using open source python including pandas, geopandas, and matplotlib. Demographic data was obtained from https://opendata.imspdx.org/ and census tract geographic datd was obtained from Oregon Metro. The resulting maps were created with matplotlib:


![image](https://user-images.githubusercontent.com/68084325/110257512-1ff38c00-7f53-11eb-841a-1ae2259ce0eb.png)

![image](https://user-images.githubusercontent.com/68084325/110257529-34378900-7f53-11eb-9ee8-aabec9a8a136.png)

![image](https://user-images.githubusercontent.com/68084325/110257554-431e3b80-7f53-11eb-9fb8-417eda669c05.png)

![image](https://user-images.githubusercontent.com/68084325/110257579-503b2a80-7f53-11eb-92de-06564ce56759.png)

![image](https://user-images.githubusercontent.com/68084325/110257590-5fba7380-7f53-11eb-98d0-ee6ac03adce9.png)

![image](https://user-images.githubusercontent.com/68084325/110257598-6b0d9f00-7f53-11eb-9c3e-92e442c68959.png)

![image](https://user-images.githubusercontent.com/68084325/110257606-782a8e00-7f53-11eb-9db3-fc738ff11be8.png)

## Custom_DEM_Toolbox
This a custom python toolbox that can be used in either Arc GIS Pro or Arc Map. The toolbox was created to automate a step in a custom digital elevation model creation workflow. This tool takes a polyline feature as input and outputs a point feature class with z-values for each feature based on a slope calculated from the input elevations. The points are always downward trending so the user should adjust the directionality of the polyline accordingly. To use this file in Arc GIS Pro, download and save as a .pyt file.
