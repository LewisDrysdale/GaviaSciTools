import os
import glob
import numpy as np
import imageio.v2 as iio

def gst_write_img_to_mp4(imgdir, processedpath):
    flderlist=glob.glob(os.path.join(imgdir,'*/'))
    writer = iio.get_writer(processedpath+'video.mp4', format='FFMPEG', fps=20)
    filelist = []
    for i in flderlist:
        fles=glob.glob(os.path.join(i,'*'))
        for im in fles:
            image=iio.imread(im)
            writer.append_data(image)
    writer.close()
    
def gst_read_image_metadata(imgdir,processedpath):

    folders=glob.glob(imgdir+'/*')
    
    for folder in folders:
        # get timestamp of picture folder
        splitname=os.path.split(folder)
        tstamp=splitname[1]
        # build filenam for saving
        savename=os.path.join(processedpath,tstamp+'-coords.csv')
        # check for existence of filename
        if not os.path.exists(savename):
    
            files=glob.glob(folder+'/*.jpg')
    
            df = pd.DataFrame(columns=['Image_Name','path', 'time','capture time','altitude', 'depth','heading','Lat','latDec','Lon','lonDec','pitch','roll','surge','sway'])
    
            loopy=range(len(files))
    
            with exiftool.ExifToolHelper() as et:
                    metadata = et.get_metadata(files)

            for i in loopy:
                file=files[i]
                files1 = [file]
                comment=metadata[i]['File:Comment']
                time = re.search('time="(.*)">', comment).group(1)
                capture_time = re.search('<capture_time>(.*)</capture_time>', comment).group(1)
                altitude = re.search('<altitude>(.*)</altitude>', comment).group(1)
                depth = re.search('<depth>(.*)</depth>', comment).group(1)
                heading = re.search('<heading>(.*)</heading>', comment).group(1)
                lat = re.search('<lat>(.*)</lat>', comment).group(1)
                lon = re.search('<lon>(.*)</lon>', comment).group(1)
                pitch = re.search('<pitch>(.*)</pitch>', comment).group(1)
                roll = re.search('<roll>(.*)</roll>', comment).group(1)
                surge = re.search('<surge>(.*)</surge>', comment).group(1)
                sway = re.search('<sway>(.*)</sway>', comment).group(1)
                
                signlat = 1
                if lat[-1] == "S":
                    signlat = -1    
                lenlat = len(lat)
                latCor = signlat * (float(lat[:2]) + float(lat[2:lenlat-2])/60.0)
    
                signlon=1
                if lon[-1] == "W":
                    signlon = -1
                lenlon = len(lon)
                lonCor = signlon * (float(lon[:3]) + float(lon[3:lenlon-2])/60.0)
    
                basename=os.path.basename(file)
                df.loc[i] = [os.path.basename(file),file,time, capture_time,altitude,depth,heading,lat,latCor,lon,lonCor,pitch,roll,surge,sway]
    
            df.to_csv(os.path.join(processedpath,tstamp+'-coords.csv'))
            
        else:
            print('file ' +savename +' exists already')