Jupyter lab notebook with Python3 source code for LEAF-Toolbox using Google Earth Engine Python API.

Note: This is an exact copy of LEAF-ToolBox-SL2P for image by image products 
as implemented on February 10, 2021 16:00 EST https://code.earthengine.google.com/fd6bddb89803bd8ea45fdcad051f75cc

You will need an Anaconda environment configured as:

>Anaconda
>>conda create --name leaftoolbox
>>conda activate leaftoolbox 
>>conda install -c conda-forge jupyterlab -y
>>conda install -c conda-forge earthengine-api -y
>>conda install -c conda-forge folium -y
>conda install -c conda-forge matplotlib -y

Then run as follows:
>Anaconda
>>conda activate leaftoolbox
>>jupyter lab

Select the notebook Leaf-Toolbox-SL2p.ipynb.
Modify code box [2] with required parameters for your processing task.
Run all
A map display will a compostite of all mapped images
A list of exported products will be reported

