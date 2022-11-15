import os
import sys
import exifread
from datetime import datetime
from dateutil.parser import parse


def exif_dump(path_name):
    """ Open image file and print EXIF tags and their values
    """
    
# Open image file for reading (must be in binary mode)
    f = open(path_name, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail',
                       'TIFFThumbnail',
                       'Filename',
                       'EXIF MakerNote'):
            print("Key: %s, Value: %s" % (tag, tags[tag]))
    f.close()


def is_datetime_tag(tag):
    """ try to find DateTime, as there are many kinds of tags"""
    return tag.find('DateTime') != -1


def get_datetime(file_handle):
    """ Must provide open image file handle for reading (must be in binary mode)
        f = open(path_name, 'rb')

        1. Get EXIF DateTimeOriginal
        2. Get other EXIF datetime
        3. Get datetime from file name
        4. Get datetime from file date
        
    """   


    exif_tag_list = []
        
    tags = exifread.process_file(file_handle, details=False)
    my_date_time = None
    my_date_time_str = ""

    # Go through EXIF tags
    datetime_original_found = False
    for tag in tags.keys():
        if 'DateTime' in tag:
            my_date_time_str = (tags[tag]).values
            my_date_time = datetime.strptime(my_date_time_str,'%Y:%m:%d %H:%M:%S')
            if 'DateTimeOriginal' in tag:                
                # print('EXIF DateTimeOrginal: ',my_date_time_str)
                
                datetime_original_found = True            
            else:                
                print("EXIF Datetime: {t}",tag,my_date_time_str)
                
        if datetime_original_found:
            break        

    # No EXIF datetime found, try to find date in filename
    if my_date_time_str == "" :
        # print("No EXIF dateTime found")
        try:
            filename = file_handle.name
            basename = os.path.basename(filename)
            file_name_date = parse(
                timestr=basename,
                fuzzy_with_tokens=True)[0]
            # print("Time parsed from name:",file_name_date)

        except Exception as e:
            print("Caught exception:",e)


    # No date in filename, then file properties time
    if my_date_time_str == "" :    
        try:
            os_time = os.path.getctime(file_handle.name)
            os_time_formatted = datetime.fromtimestamp(os_time).strftime('%Y:%m:%d %H:%M:%S')
            # print("OS time formatted:", os_time_formatted)
            my_date_time_str = os_time_formatted
        except Exception as e:
            print("Caught exception:",e)

    my_date_time = datetime.strptime(my_date_time_str,'%Y:%m:%d %H:%M:%S')
    return my_date_time

def get_y_ym_dirname_from_datetime( dt ):
    year=dt.year
    month=dt.month
    return "{:04d}\\{:04d}-{:02d}".format(year,year,month)


def make_datetime(datestring): # date_obj = 
    return parse(datestring)

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
            



