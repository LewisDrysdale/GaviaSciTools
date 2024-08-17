import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as et

# sbe19plus data
def concat_ascii_data(ddir):
    fls=glob.glob(ddir)
    # concantenate the dat files
    for i,nme in enumerate(fls):
        data=pd.read_fwf(nme)
        if i==0:
            alldata=data
        else:
            alldata=pd.concat([alldata,data])

    alldata=alldata[['Sal00', 'DepSM','PrdM','Tv290C']]
    
    return alldata



### GAVIA CTD data
def readctdlog(ldir,processedpath):    # get list of files
    ctdfiles=os.path.join(ldir,'*ctd-slocum*.xml')
    flelist=glob.glob(ctdfiles)
        
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        xml = et.parse(fles)
        element=xml.getroot().find('entry')
        if element:
            if count==0:
                ctdf=pd.read_xml(fles)
            else:
                df=pd.read_xml(fles,names=None)
                ctdf=pd.concat([ctdf,df],ignore_index=True)
    # save as .csv file
    ctdf.to_csv(os.path.join(processedpath,'CTDdata.csv'))   

    return ctdf

### GAVIA autopilot data
def readautolog(ldir,processedpath):    # get list of files
    apfiles=os.path.join(ldir,'*autopilot*.xml')
    flelist=glob.glob(apfiles)
        
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        xml = et.parse(fles)
        element=xml.getroot().find('entry')
        if element:
            if count==0:
                apdf=pd.read_xml(fles)
            else:
                df=pd.read_xml(fles,names=None)
                apdf=pd.concat([apdf,df],ignore_index=True)
    # save as .csv file
    apdf.to_csv(os.path.join(processedpath,'autopilotdata.csv'))   

    return apdf

### GAVIA missionmanager data
def readmmlog(ldir,processedpath):    # get list of files
    apfiles=os.path.join(ldir,'*missionmanager*.xml')
    flelist=glob.glob(apfiles)
        
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        xml = et.parse(fles)
        element=xml.getroot().find('entry')
        if element:
            if count==0:
                mmdf=pd.read_xml(fles)
            else:
                df=pd.read_xml(fles,names=None)
                mmdf=pd.concat([mmdf,df],ignore_index=True)
    # save as .csv file
    mmdf.to_csv(os.path.join(processedpath,'missionmanager.csv'))   

    return mmdf

# NAV LOG IS MORE COMPLEX XML THAT CANT BE READ BY THE PANDAS READ_XML SO NEED TO EXTRACT VARIABLES THEN MERGE WITH DATASTE CREATED BY READ_XML
def readnavlog(ldir,processedpath):    # get list of files
    navfiles=os.path.join(ldir,'*navigator*.xml')
    flelist=glob.glob(navfiles)

    # for each file, read to pandas dataframe and concatenate
    for count, files in enumerate(flelist):
        if count==0:
            rtdf=pd.read_xml(files)
            tree = et.parse(files)
            root = tree.getroot()

            drheading = []
            drvelocity=[]
            drpitch=[]
            droll=[]
            drlat = []
            drlon=[]
            heading=[]
            pitch=[]
            roll=[]
            depth=[]
            velocity=[]
            lat=[]
            lon=[]

            for node in root.findall("./entry/dead-reckoning-orientation/heading"):
                drheading.append(node.text)

            for node in root.findall("./entry/dead-reckoning-orientation/pitch"):
                drpitch.append(node.text)

            for node in root.findall("./entry/dead-reckoning-orientation/roll"):
                droll.append(node.text)

            for node in root.findall("./entry/dead-reckoning-velocity/surge"):
                drvelocity.append(node.text)           
                
            for node in root.findall("./entry/velocity/surge"):
                velocity.append(node.text)            
                
            for node in root.findall("./entry/dead-reckoning-position/lon"):
                drlon.append(node.text)

            for ptch in root.findall("./entry/dead-reckoning-position/lat"):
                drlat.append(ptch.text)

            for node in root.findall("./entry/orientation/heading"):
                heading.append(node.text)

            for node in root.findall("./entry/orientation/pitch"):
                pitch.append(node.text)

            for node in root.findall("./entry/orientation/roll"):
                roll.append(node.text)

            for node in root.findall("./entry/position/depth"):
                depth.append(node.text)

            for node in root.findall("./entry/position/lat"):
                lat.append(node.text)

            for ptch in root.findall("./entry/position/lon"):
                lon.append(ptch.text)    

            nddf = pd.DataFrame(
                                   list(zip(drheading,drvelocity, drpitch, droll,drlat,drlon,velocity,heading, pitch, roll,depth,lat, lon)), 
                                   columns=['DRHeading', 'DRVelocity','DRPitch', 'DRRoll','DRLat','DRLon','speed','Heading','Pitch','Roll','Depth','Lat','Lon'])  

            nvdf=pd.concat([rtdf, nddf], axis=1)

        else:
            rtdf=pd.read_xml(files,names=None)
            tree = et.parse(files)
            root = tree.getroot()

            drheading = []
            drvelocity=[]
            drpitch=[]
            droll=[]
            drlat = []
            drlon=[]
            heading=[]
            pitch=[]
            roll=[]
            depth=[]
            velocity=[]
            lat=[]
            lon=[]

            for node in root.findall("./entry/dead-reckoning-orientation/heading"):
                drheading.append(node.text)

            for node in root.findall("./entry/dead-reckoning-orientation/pitch"):
                drpitch.append(node.text)

            for node in root.findall("./entry/dead-reckoning-orientation/roll"):
                droll.append(node.text)

            for node in root.findall("./entry/dead-reckoning-velocity/surge"):
                drvelocity.append(node.text)           
                
            for node in root.findall("./entry/velocity/surge"):
                velocity.append(node.text)
            
            for node in root.findall("./entry/dead-reckoning-position/lon"):
                drlon.append(node.text)

            for ptch in root.findall("./entry/dead-reckoning-position/lat"):
                drlat.append(ptch.text)

            for node in root.findall("./entry/orientation/heading"):
                heading.append(node.text)

            for node in root.findall("./entry/orientation/pitch"):
                pitch.append(node.text)

            for node in root.findall("./entry/orientation/roll"):
                roll.append(node.text)

            for node in root.findall("./entry/position/depth"):
                depth.append(node.text)

            for node in root.findall("./entry/position/lat"):
                lat.append(node.text)

            for ptch in root.findall("./entry/position/lon"):
                lon.append(ptch.text)    
            

            
            nddf = pd.DataFrame(
                                   list(zip(drheading,drvelocity, drpitch, droll,drlat,drlon,velocity,heading, pitch, roll,depth,lat, lon)), 
                                   columns=['DRHeading', 'DRVelocity','DRPitch', 'DRRoll','DRLat','DRLon','speed','Heading','Pitch','Roll','Depth','Lat','Lon'])  

            
            df=pd.concat([rtdf, nddf], axis=1)

            nvdf=pd.concat([nvdf,df],ignore_index=True)            
                 
    labels = ['build-number',
                'build-tag',
                'calculate-magnetic-deviation',
                'max-valid-depth', 
                'dvl-timeout',
                'gps-timeout',
                'gps-validation-enabled',
                'veto-use-water-velocity',
                'station-keeping-enabled',
                'sound-velocity-timeout',
                'temperature-timeout',
                'seanav-timeout',
                'use-pressure',
                'max-allowed-variance',
                'pressure-timeout',
                'compass-timeout',
                'dead-reckoning-sog-timeout',
                'variance-exceeded-warning-level',
                'max-dead-reckoning-distance',
                'pressure-depth-conversion',
                'use-water-velocity',
                'density-abort-limit',
                'gps-variance',
                'lbl-variance',
                'revolutions-bias',
                'revolutions-scale',
                'dvl-bias',
                'dvl-scale',
                'gyro-bias',
                'control-rate',
                'motor-default',
                'stationary-radius',
                'stationary-p',
                'stationary-idle',
                'stationary-depth-timeout',
                'estimate-speed',
                'detect-ins-type',
                'ins-detect-timeout',
                'override-propulsion-ip',
                'observe-timer-on',
                'predict-timer-on',
                'binary-log',
                'broadcast-interface',
                'broadcast-enable',
                'broadcast-frequency',
                'broadcast-navigation-message',
                'broadcast-ins-enabled',
                'broadcast-depth-message',
                'broadcast-sound-velocity-message',
                'rate',
                'control-priority',
                'control-priority-time',
                'idle-status',
                'last-command-elapsed',
                'maxWarningLevel',
                'pilot-status',
                'valid',
                'zero-altitude']
    
    nvdf=nvdf.drop(labels, axis=1)    
    nvdf["Lat"]=nvdf["Lat"].astype(str).str.replace('N', '')
    nvdf["Lon"]=nvdf["Lon"].astype(str).str.replace('W', '')
    nvdf["DRLat"]=nvdf["DRLat"].astype(str).str.replace('N', '')
    nvdf["DRLon"]=nvdf["DRLon"].astype(str).str.replace('W', '')


    for index, row in nvdf.iterrows():
        lat=row['Lat']
        if len(lat)>4:
            signlat = 1   
            lenlat = len(lat)
            latCor = signlat * (float(lat[:2]) + float(lat[2:lenlat-2])/60.0)
            # nvdf.Lat[index]=str(latCor)
            df.loc[index, 'Lat']=str(latCor) 
            
        lon=row['Lon']
        if len(lat)>4:
            signlat = 1   
            signlon = -1
            lenlon = len(lon)
            lonCor = signlon * (float(lon[:3]) + float(lon[3:lenlon-2])/60.0)
            df.loc[index, 'Lon']=str(lonCor) 
            # nvdf.Lon[index]=str(lonCor)        
    
    # CONVERT DATA TO NUMERIC 
    cols=[i for i in nvdf.columns if i not in ["time","timestamp"]]
    for col in cols:
        nvdf[col]=pd.to_numeric(nvdf[col], errors="ignore",downcast='float')    
    
    # DOESNT WORK WITH LAT LONG (JUTS NOW) SO CONVERT TO FLOAT AGAIN!!
    # nvdf["Lat"]=nvdf["Lat"].astype(float)
    nvdf["Lon"]=nvdf["Lon"].astype(float)
    nvdf["DRLat"]=nvdf["DRLat"].astype(float)
    nvdf["DRLon"]=nvdf["DRLon"].astype(float)
    
    # save as .csv file
    # newstr = missionname.replace("_", "-")
    nvdf.to_csv(os.path.join(processedpath,'NAVdata.csv')) 

    # drop unwanted variables form nav data
    nvdf=nvdf.drop(columns=[
         'magnetic-deviation',
         'pressure-warnings',
         'lat-lon-precision',
         'average-water-density',
         'sound-velocity',
         'center-actuators-on-idle',
         'dead-reckoning-orientation',
         'dead-reckoning-velocity',
         'orientation',
         'position',
         'variance',
         'velocity'])

    # rename duplicat variables (t,s, sv, from control module?
    nvdf=nvdf.rename(columns={"time": "time-nav",
                              "salinity": "salinity-nav",
                              "temperature": "temperature-nav",
                              "sound-velocity": "sound-velocity-nav"})
    
    return nvdf



### GPS data
def readgpslog(ldir,processedpath):    # get list of files
    files=os.path.join(ldir,'*gps-*.xml')
    flelist=glob.glob(files)
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        if count==0:
            gpdf=pd.read_xml(fles)
        else:
            df=pd.read_xml(fles,names=None)
            gpdf=pd.concat([gpdf,df],ignore_index=True)
    # save as .csv file
    os.makedirs('data/nav-files', exist_ok=True)  
    gpdf.to_csv(os.path.join(processedpath,'GPSdata.csv'))     
    gpdf=gpdf.drop(columns=[
         'build-number',
         'build-tag',
         'log-level',
         'rate',
         'sbf-remote-com-port',
         'sbf-local-com-port',
         'vsp-local-com-port',
         'corrections-local-com-port',
         'vsp-local-tcp-port',
         'corrections-local-udp-port',
         'vsp-enabled',
         'corrections-enabled',
         'sbf-enabled',
         'sbf-unicast-enabled',
         'sbf-unicast-port',
         'sbf-unicast-interface',
         'log-nmea',
         'log-messages',
         'multicast-receive-enabled',
         'multicast-receive-port',
         'multicast-receive-addr',
         'multicast-receive-interface',
         'messages-received',
         'raw-logged-bytes',
         'received-telnet-bytes',
         'sent-corr-bytes',
         'sent-corr-packets',
         'sent-telnet-bytes',
         'time-since-gga',
         'time-since-sent',
         'diff-age',
         'sats',
         'stnRef',
         'cogt',
         'lat-dev',
         'lon-dev',
         'sogk',
         'sogm'])

    return gpdf

### SBP data
def readsbplog(ldir,processedpath):    # get list of files
    files=os.path.join(ldir,'*sbp*.xml')
    flelist=glob.glob(files)
    sbpdf = pd.DataFrame()
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        xml = et.parse(fles)
        element=xml.getroot().find('entry')
        if element:
            if count==0:
                sbpdf=pd.read_xml(fles)
            else:
                df=pd.read_xml(fles,names=None)
                sbpdf=pd.concat([sbpdf,df],ignore_index=True)
    # save as .csv file
    sbpdf.to_csv(os.path.join(processedpath,'SBPdata.csv'))       
    return sbpdf

### AANDERAA data
def readaandlog(ldir,processedpath):    # get list of files
    files=os.path.join(ldir,'*aanderaa*.xml')
    flelist=glob.glob(files)
    aandf = pd.DataFrame()
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        xml = et.parse(fles)
        element=xml.getroot().find('entry')
        if element:
            if count==0:
                aandf=pd.read_xml(fles)
            else:
                df=pd.read_xml(fles,names=None)
                aandf=pd.concat([aandf,df],ignore_index=True)
    # save as .csv file
    aandf.to_csv(os.path.join(processedpath,'aanderaadata.csv'))   
    return aandf

### ECOPUCK data
def readecolog(ldir,processedpath):    # get list of files
    files=os.path.join(ldir,'*ecopuck-flntu*.xml')
    flelist=glob.glob(files)
    ecopuck = pd.DataFrame()
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        xml = et.parse(fles)
        element=xml.getroot().find('entry')
        if element:
            if count==0:
                ecopuck=pd.read_xml(fles,names=[
                                        "tstamp", "t",
                                        "chl-raw",
                                        "chl-ref","date", "ntu-raw",
                                        "ntu-ref","thermistor"])
            else:
                df=pd.read_xml(fles,names=["tstamp", "t",
                                            "chl-raw",
                                           "chl-ref","date", "ntu-raw",
                                           "ntu-ref","thermistor"])
                ecopuck=pd.concat([ecopuck,df],ignore_index=True)

    ecopuck = ecopuck.drop('date', axis=1)
    ecopuck=ecopuck.rename(columns={"tstamp": "timestamp", "t": "time"})

    # Chlorophyll Scale Factor
    CHLDarkCounts=50
    CHLScaleFactor=0.0121
    CHLMaxOut=4130
    CHLRes=1
    CHL = CHLScaleFactor*(ecopuck["chl-raw"]-CHLDarkCounts)
    
    # Nephelometric Turbidity Unit
    NTUDarkCounts=51
    NTUSolutionValue=1784
    NTUScaleFactor=0.0249
    MaxOut=4130
    Res=1
    NTU = NTUScaleFactor*(ecopuck["ntu-raw"]-NTUDarkCounts)
    
    # Adding a new column chl-corrected with values
    ecopuck['chl-corrected']=CHL.values
    ecopuck['ntu-corrected']=NTU.values

    # save as .csv file
    ecopuck.to_csv(os.path.join(processedpath,'ecopuckdata.csv'))   
    return ecopuck