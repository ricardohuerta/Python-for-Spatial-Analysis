# Spatial Analysis and Tools in Python
I will use this repository to track my forays in to spatial analysis using python.

# AP_Tool
This is a python toolbox developed for modelling wireless signal in outdoor environment. The tool completes the following steps:

1. Calculates visible areas based on a wirelss signal access point
2. Calculates distance and Free Space Path Loss
3. Calculates signal loss due to object interference
4. Ouputs a raster representing signal power radiating from the input point

This tool can be implemented in ArcGIS Pro. 

## Example outputs

![AllPoints](https://user-images.githubusercontent.com/68084325/134940994-e91ebd92-2ec9-4c17-9a4d-6d4cf1bb8b3d.jpg)

![PriorityArea](https://user-images.githubusercontent.com/68084325/134941025-15293fc8-4fdb-4f9e-becc-6c525b26baeb.jpg)

# Street Tree Inventory for the City of Wilsonville
This is a data analysis for the street trees of Wilsonville. We collected all of the tree data through fieldwork and assessed general street tree population and damage caused by the 2020 ice storm. Data visualization was completed with matplotlib and seaborn packages. Statistical analysis completed in pandas.

## Deciduous vs. Coniferous Stree Trees

![tree_types](https://user-images.githubusercontent.com/68084325/134935742-aaf2b886-0a70-48c2-b800-6590025be09d.png)

## Damage Categories Across All Street Trees

![status_across_trees](https://user-images.githubusercontent.com/68084325/134935838-dc9c0d5c-88fa-49b1-80be-60fe337a53bc.png)

## Most Removed Species

![most_removed_raw_species](https://user-images.githubusercontent.com/68084325/134936193-6c8e3336-b66b-4fde-af00-c5921570c285.png)

## Species with Highest Rate of Removal

![removal_rates_species](https://user-images.githubusercontent.com/68084325/134936333-6e9f3c33-3654-4a69-957e-4082d23a7928.png)

## Species with Highest Rate of Storm Damage

![damage_rates_species](https://user-images.githubusercontent.com/68084325/134936806-18f47461-29d3-44b6-a8c3-60ec7d8a9aae.png)

## Most Added Tree Species

![most_added_raw_species](https://user-images.githubusercontent.com/68084325/134936941-c773a9fc-a130-43f3-95c2-d03934af4d6a.png)

## Diameter at Breast Height Across Damage Status Categories

![DBH_status_dist](https://user-images.githubusercontent.com/68084325/134937104-3372d177-8acc-4ca1-beb1-2874eb00832f.png)

## Diameter at Breast Height for Removed vs. Not Removed Trees

![removed_noRemoved_kde](https://user-images.githubusercontent.com/68084325/134937289-56e220ce-da33-451f-b796-ae3dcc1b7d85.png)

## Diameter at Breast Height for Removed Street Trees

![DBH_removed](https://user-images.githubusercontent.com/68084325/134937457-14f422dc-5a62-485c-90b7-f892cb9848bf.png)

## Removed Tree Heatmap

![DBH_removed_heatmap](https://user-images.githubusercontent.com/68084325/134937582-f3dabd20-e9c4-44b4-8514-c498ae765b46.png)


# Arc GIS Pro Tools
These are simple tools I created to perform common spatial analysis and manipulation tasks for Arc GIS Pro. 
 
# Social Vulnerability Analysis
This is a social vulnerability analysis for county census tracts in the Portland Metro Statistical Area using open source python including pandas, geopandas, and matplotlib. Demographic data was obtained from https://opendata.imspdx.org/ and census tract geographic datd was obtained from Oregon Metro. The resulting maps were created with matplotlib:


![image](https://user-images.githubusercontent.com/68084325/110257512-1ff38c00-7f53-11eb-841a-1ae2259ce0eb.png)

![image](https://user-images.githubusercontent.com/68084325/110257529-34378900-7f53-11eb-9ee8-aabec9a8a136.png)

![image](https://user-images.githubusercontent.com/68084325/110257554-431e3b80-7f53-11eb-9fb8-417eda669c05.png)

![image](https://user-images.githubusercontent.com/68084325/110257579-503b2a80-7f53-11eb-92de-06564ce56759.png)

![image](https://user-images.githubusercontent.com/68084325/110257590-5fba7380-7f53-11eb-98d0-ee6ac03adce9.png)

![image](https://user-images.githubusercontent.com/68084325/110257598-6b0d9f00-7f53-11eb-9c3e-92e442c68959.png)

![image](https://user-images.githubusercontent.com/68084325/110257606-782a8e00-7f53-11eb-9db3-fc738ff11be8.png)

# Custom_DEM_Toolbox
This a custom python toolbox that can be used in either Arc GIS Pro or Arc Map. The toolbox was created to automate a step in a custom digital elevation model creation workflow. This tool takes a polyline feature as input and outputs a point feature class with z-values for each feature based on a slope calculated from the input elevations. The points are always downward trending so the user should adjust the directionality of the polyline accordingly. To use this file in Arc GIS Pro, download and save as a .pyt file.

# LCEP_PublicLandOwnership
These are a collection of scripts documenting the methods I used in a land onwership analysis of the Lower Columbia floodplain. They are not applicable as standalone scripts and are meant nearly as a way to to document the methods/workflows used in the analysis. The resulting web map can be viewed at: 
https://portlandcc.maps.arcgis.com/apps/instant/interactivelegend/index.html?appid=9e518b772da2422cbac13133c85267b1 
