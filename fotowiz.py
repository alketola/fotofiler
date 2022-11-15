# Photo collection reordering wizard
#
# 1. Ask to select source directory
# 2. Find files
#       Find dates
# 3. Calculate new paths and filenames
# 4. Ask to select destination directory
# 5. Create destination tree
# 6. Preview. OK=> continue, NOK=> Back
# 7. Create command queue
# 8. Display progress bar
# 9. Execute commands

print('Photo copy wizard by Antti Ketola 2022')
# Windows version

import os
import glob
import easygui
import pprint
from pprint import pprint
import fotoinfo
from fotoinfo import FotoInfo
##import icecream
##from icecream import ic
##icecream.install()
import fotoexif
from fotoexif import *

# Ask source directory, from where files are copied
source_dir = easygui.diropenbox(title="Please input source folder of photos")
if source_dir is None:
    print("No source folder selected, exiting")
    exit
else:
    print("Source dir",source_dir)

source_path = os.path.join(source_dir,'**\\*.*') # not NoneType!!
print("Source_path",source_path)

# Ask destination directory, where files are copied to
dest_root = easygui.diropenbox(title="Please input destination folder of photos",
                                   default="C:\\")

if dest_root is None:
    print("No destination folder selected, exiting")
    exit
else:
    print("Destination folder",dest_root)

fotos_list = []
datum = ""
count = 0
for filename in glob.iglob(source_path, recursive=True):        
    file=open(filename,'rb')
    print('----')
    print(file.name,"***")
    datum=get_datetime(file)
    dest_dir = get_y_ym_dirname_from_datetime(datum)
    #print(dir_name)
    info=FotoInfo(source_path,datum,dest_root,dest_dir,os.path.basename(file.name))
    fotos_list.append(info)
    file.close()
    count = count+1
    if count > 10:
        break
    
print("Number of files to copy:", len(fotos_list))
# pprint.pprint(files_to_copy)




