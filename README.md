Gavia-Science-Tools
==============================

Creating a virtual environment using [this help](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)

`conda create -n myenv python=3.8`



Process and analyse data from Teledyne Gavia Offshore Surveyor

gst_read_functions.gst_unzip_log_data(“log data path”)

    inputs: absolute path to folder containing .xml log files
    
gst_read_functions.gst_read_log_data(logdir, savedir, types) 

    inputs: absolute path to folder containing .xml log files, absolute path to folder where processed data is to be saved, list of sensor data to be processed

I was having issues when developing the functions used to process that data. Running 

    python setup.py clean --all
    python setup.py develop
    
seemed to resolve the problem.
