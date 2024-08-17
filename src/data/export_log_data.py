import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import src.data.gst_sub_functions as rfuncs

def export_log_data(logdir,processedpath):

    files=glob.glob(logdir+'\*ctd*')
    if files:
    # read CTD data and convert to .csv format, output to data/ctd-files/
        ctdf=rfuncs.readctdlog(logdir,processedpath)

    files=glob.glob(logdir+'\*sbp*')
    if files:
        # read SBP data and convert to .csv format, output to data/sbp-files/
        sbpdf=rfuncs.readsbplog(logdir,processedpath)

    files=glob.glob(logdir+'\*gps*')
    if files:    
        # read GPS data and convert to .csv format, output to data/gps-files/
        gpdf=rfuncs.readgpslog(logdir,processedpath)

    files=glob.glob(logdir+'\*nav*')
    if files: 
        # read nav data and convert to .csv format, output to data/nav-files/
        nvdf=rfuncs.readnavlog(logdir,processedpath)

    files=glob.glob(logdir+'\*aanderaa*')
    if files: 
        # read aanderaa data and convert to .csv format, output to data/aanderaa-files/
        aandf=rfuncs.readaandlog(logdir,processedpath)

    return nvdf, gpdf