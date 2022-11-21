import os
import sys
import exifread
from datetime import datetime
from dateutil.parser import parse
from pathlib import Path


def exif_dump(path_name):
    """ Open image file and print EXIF tags and their values

    >>> exif_dump('./test/assets/EXIFTEST2.JPG')
    Key: Image ExifOffset, Value: 26
    Key: EXIF DateTimeDigitized, Value: 2022:11:16 01:26:18
    >>> exif_dump('./test/assets/EXIFTEST1.JPG')
    Key: Image DateTime, Value: 2022:11:16 01:23:45
    Key: Image ExifOffset, Value: 58
    Key: EXIF DateTimeOriginal, Value: 2022:11:16 01:02:34
    Key: EXIF DateTimeDigitized, Value: 2022:11:16 01:20:48
    >>> exif_dump('./test/assets/RED_IMAGE_20201023.jpg')    
    """
    ##>>> exif_dump('./test/assets/txt.txt') yields nothing but error: File format not recognized.
    
    # Open image file for reading (must be in binary mode)
    try:
        f = open(path_name, 'rb')

        # Return Exif tags
        tags = exifread.process_file(f)
        for tag in tags.keys():
##            if tag not in ('JPEGThumbnail',
##                           'TIFFThumbnail',
##                           'Filename',
##                           'EXIF MakerNote'):
                print("Key: %s, Value: %s" % (tag, tags[tag]))
    except Exeption as e:
        print(f"exif_dump({path_name}) hit by exception {e}")
                
    finally:
        f.close()


def is_datetime_tag(tag):
    """
    Try to find DateTime, as there are many kinds of tags

    >>> is_datetime_tag("DateTimeOriginal")
    True
    >>> is_datetime_tag("DateBar")
    False
    >>> is_datetime_tag("FOO DateTimeBar Tag")
    True

    """
    return tag.find('DateTime') != -1


def get_datetime(file_handle):
    """ Must provide open image file handle for reading (must be in binary mode)
        f = open(path_name, 'rb')

        1. Get EXIF DateTimeOriginal
        2. Get other EXIF datetime
        3. Get datetime from file date (oldest available)
        4. Get datetime from file name
        


    >>> fhandle = open('./test/assets/EXIFTEST1.JPG','rb')
    >>> get_datetime(fhandle)
    datetime.datetime(2022, 11, 16, 1, 2, 34)
    >>> fhandle.close()
    >>>

    >>> fhandle = open('./test/assets/EXIFTEST2.jpg','rb')
    >>> get_datetime(fhandle)
    datetime.datetime(2022, 11, 16, 1, 26, 18)
    >>> fhandle.close()
    >>>

    >>> fhandle = open('./test/assets/RED_IMAGE_20201023.jpg','rb')
    >>> get_datetime(fhandle)
    datetime.datetime(2022, 11, 16, 1, 40, 16)
    >>> fhandle.close()
    >>>

    >>> fhandle = open('./test/assets/txt.txt','rb')
    >>> get_datetime(fhandle)
    datetime.datetime(2022, 11, 16, 1, 57, 13)
    >>> fhandle.close()
    >>>
    """   

    exif_tag_list = []
        
    my_date_time = None
    my_date_time_str = ""
    
    # Find file name
    filename = file_handle.name
    basename = os.path.basename(filename)
    
    # Find file type
    suf = Path(filename).suffix

    if suf in ['.jpg','.JPG','.tif','.TIF','.wav','.WAV','.jpeg','.JPEG','.tiff','.TIFF','.heif','.heic']:
    # Go through EXIF tags, in the types above
        tags = exifread.process_file(file_handle, details=False)
        datetime_original_found = False
        try:
            for tag in tags.keys():
                if 'DateTime' in tag:
                    my_date_time_str = (tags[tag]).values
                    my_date_time = datetime.strptime(my_date_time_str,'%Y:%m:%d %H:%M:%S')
                    if 'DateTimeOriginal' in tag:                
                        # print('EXIF DateTimeOrginal: ',my_date_time_str)
                        
                        datetime_original_found = True            
                    else:
                        pass
                        # print("EXIF Datetime: {t}",tag,my_date_time_str)
                        
                if datetime_original_found:
                    break
        except Exception as e:
            print("EXIF tags processing exception:",e)

    # if no date in filename, then fall back to file properties time. Take oldest of creation or modification date.
    if my_date_time == None :    
        try:
            # smallest (earliest) of the two possible (not considering last access time, no way)            
            os_time_c = os.path.getctime(file_handle.name)
            os_time_m = os.path.getmtime(file_handle.name)  
            if os_time_c < os_time_m:
                os_time = os_time_c
            else:
                os_time = os_time_m                
        except Exception as e:
            print("getctime / getmtime: Caught exception:",e)
            print("Fall back to Epoch!")
            os_time = 0 # Fall back to Epoch if nothing was found, so you will find date and dirs for 1970-01-01

        try:    
            os_time_formatted = datetime.fromtimestamp(os_time).strftime('%Y-%m-%d %H:%M:%S')
            # print("OS time formatted:", os_time_formatted)
            my_date_time_str = os_time_formatted
            my_date_time = datetime.strptime(my_date_time_str,'%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print("time formatting: Caught exception:",e)
            print("Fall back to Epoch!")
            os_time = 0 # Fall back to Epoch if nothing was found, so you will find date and dirs for 1970-01-01
            os_time_formatted = "1970-01-01 00:00:01"
            my_date_time = datetime(1970,1,1,0,0,1)


    # No EXIF datetime found, try to find date in filename
    if my_date_time == None :
        # print("No EXIF dateTime found")
        try:
            my_date_time = parse(
                timestr=basename,
                fuzzy_with_tokens=True)[0]
            # print("Time parsed from name:",file_name_date)

        except Exception as e:
            pass
            # print("Filename: Caught exception:",e)

            
    if my_date_time == None :
        print('\tUnlikely ERROR: Photo date not found ')
    
    return my_date_time

def get_y_ym_dirname_from_datetime( dt ):
    year=dt.year
    month=dt.month
    return "\\{:04d}\\{:04d}-{:02d}".format(year,year,month)


def make_datetime(date_string):
    """
    A shorthand to make datetime object from date String

    >>> dt=make_datetime('2022-11-16 01:02')
    >>> dt
    datetime.datetime(2022, 11, 16, 1, 2)

    """
    
    return parse(date_string)

# datetime.strptime(datestring, '%Y:%m:%d %H:%M:%S')


def exif_my_tags(file_handle):
# Must provide open image file handle for reading (must be in binary mode)
# f = open(path_name, 'rb')
    exif_tag_list = []
        
    tags = exifread.process_file(file_handle, details=False)
    for tag in tags.keys():
        if tag in ( 'GPS GPSLongitude',
                    'GPS GPSLatitudeRef',
                    'GPS GPSDate',
                    'GPS GPSTimeStamp',
                    'GPS GPSAltitudeRef',
                    'GPS GPSLongitudeRef',
                    'GPS GPSLatitude',
                    'Image GPSInfo'
                   ):
            exif_tag_list.append((tag, tags[tag]))
            # # print("Key: %s, Value: %s" % (tag, tags[tag]))
                        
    return dict(exif_tag_list)
            

if __name__ == "__main__":
    import doctest
    doctest.testmod()

