import os
import matplotlib.pyplot as plt
import pandas as pd
import glob
import cmocean as cmo
import sys
sys.path.append('../')
import src.data.export_log_data as efuncs
import src.data.gst_sub_functions as rfuncs

def gst_unzip_log_data(logdir):
    ## Unzip all the files (if not unzipped already)
    ## ALL DATA
    files=glob.glob(logdir+'/*xml*')# list files
    if files:
    # determine if files are zipped. If yes, unzip, if no, continue
        allfiles=os.path.join(logdir,'*.xml.gz')    
        import gzip, shutil
        flelist=glob.glob(allfiles)
        for i in flelist:
            xfle=os.path.splitext(i)[0]
            if not os.path.isfile(xfle):
                with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)



def gst_read_log_data(logdir, savedir, types):

    for i in types:
        files=glob.glob(logdir+'/*'+i+'*')
        if files:
            if i == 'missionmanager':
                mmdf=rfuncs.readmmlog(logdir,savedir)
            elif i == 'autopilot':
                apdf=rfuncs.readautolog(logdir,savedir)
            elif i == 'ctd':
                ctdf=rfuncs.readctdlog(logdir,savedir)    
            elif i == 'gps':
                gpdf=rfuncs.readgpslog(logdir,savedir)            
            elif i == 'sbp':
                sbpdf=rfuncs.readsbplog(logdir,savedir)            
            elif i == 'nav':
                nvdf=rfuncs.readnavlog(logdir,savedir)            
            elif i == 'aanderaa':
                aandf=rfuncs.readaandlog(logdir,savedir)
            elif i == 'ecopuck':
                ecopuck=rfuncs.readecolog(logdir,savedir)

                
    # create merged file
    ## always gps and nav log to mege first to new df
    # round timestamp to o decimal places ready for merging
    nvdf=nvdf.round({'timestamp': 0})
    gpdf=gpdf.round({'timestamp': 0})
    gpdf=gpdf.rename(columns={"time": "time-gps"})
    
    # Mmerge nav data and gps
    auvmerge=pd.merge(nvdf, gpdf,how='outer',on='timestamp')

    ## create null values for datasets, 
    ## so we can check for existence of data
    ctdf=pd.DataFrame()
    sbpdf=pd.DataFrame()
    gpdf=pd.DataFrame()
    nvdf=pd.DataFrame()
    aandf=pd.DataFrame()               
    ecopuck=pd.DataFrame()

    # ctd
    if not ctdf.empty:
        ctdf=ctdf.round({'timestamp': 0})
        ctdf=ctdf.rename(columns={"time": "time-ctd"})
        auvmerge=pd.merge(auvmerge, ctdf,how='outer',on='timestamp')
    
    # aandera 
    if not aandf.empty:
        aandf=aandf.round({'timestamp': 0})
        aandf=aandf.rename(columns={"time": "time-aand"})
        auvmerge=pd.merge(auvmerge, aandf,how='outer',on='timestamp')
    
    # ecopuck 
    if not ecopuck.empty:
        ecopuck=ecopuck.round({'timestamp': 0})
        ecopuck=ecopuck.rename(columns={"time": "time-eco"})
        auvmerge=pd.merge(auvmerge, ecopuck,how='outer',on='timestamp')
    
    # sbp 
    if not sbpdf.empty:
        print('to be done later, when we have some data')          
    
    auvmerge.to_csv(os.path.join(savedir,'auvdata.csv')) 