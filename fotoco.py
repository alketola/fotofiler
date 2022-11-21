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
import shutil
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

def build_fotos_list(source_dir, recurse, dest_dir):
    """
    Searchs files from source dir, and create list of FotoInfo objects,
    and a list of destination directories to be created.

    >>> L, dirs = build_fotos_list("test/assets/EXIFTEST1.JPG",False,"test/assets")
    >>> len(L)
    1
    >>> len(dirs)
    1
    >>> L[0].filename
    'EXIFTEST1.JPG'
    >>> dirs.pop()
    '\\2022\\2022-11'
    """
    foto_list = []
    dest_dir_set = set()                                         
    for filename in glob.iglob(source_dir, recursive=recurse):        
        file=open(filename,'rb')
        # print('.',end="") # progress indication
        # print(file.name,"***")
        datum=get_datetime(file)
        dest_dir = get_y_ym_dirname_from_datetime(datum)
        dest_dir_set.add(dest_dir)
        info=FotoInfo(filename,
                      datum,
                      dest_root,
                      dest_dir,
                      os.path.basename(file.name)
                      )
        foto_list.append(info)
        file.close()

    return (foto_list, dest_dir_set)



# Begin!

welcome_msg="""Hello and welcome to copy photo files!

               All files are copied, anyway, from the source.
               The files are then arranged to a tree, according to
               date.

               The basic case makes directories of years,
               and inside them, there are subdirectories
               for each month

               The file date is deduced from:
               1. EXIF DateTimeOriginal
               2. EXIF other DateTime
               3. File name
               4. File creation time (oldest date in file metadata)
            """
easygui.msgbox(welcome_msg,"photoco.py by Antti Ketola 2022")

# Ask source directory, from where files are copied
source_dir = easygui.diropenbox(title="Please input source folder of photos")
if source_dir is None:
    print("No source folder selected, exiting")
    exit
else:
    print("Source dir",source_dir)

source_spec = os.path.join(source_dir,'**\\*.*') 
print("Source_path",source_spec)

# Ask destination directory, where files are copied to
dest_root = easygui.diropenbox(title="Please input destination folder of photos",
                                   default="C:\\")

if dest_root is None:
    print("No destination folder selected, exiting")
    exit
else:
    print("Destination folder",dest_root)

print("Analysing... this may take a while")

fotos_list = []

fotos_list, dest_dir_set = build_fotos_list(source_spec,
                                            recurse=True,
                                            dest_dir=dest_root)
    
print("Number of files to copy:", len(fotos_list))
dest_contents = os.listdir(dest_root)

if len(dest_contents)==0:
    dest_description = "is empty"
else:
    dest_description = f"already has {len(dest_contents)} files"
print(f'The files will be copied and directories created in {dest_root}, which {dest_description}')

title = 'Start copying?'
message = "Destination: root="+dest_root+"\n"
message +="   following subdirs will be created:\n"
for d in dest_dir_set:
    message += d+'\n'
go_copy = easygui.ccbox(message, title)

if not go_copy:
    print("Cancelled.")
    quit()

# Create dirs
print("Creating directories")
for d in dest_dir_set:
    os.makedirs(dest_root+d, exist_ok=True)


# Copy photos
print("Copying")
copied_count=0
for f in fotos_list:
    shutil.copy2(f.source_path,f.full_dest_path)
    copied_count = copied_count+1
    print('.',end='')

message = "Copying Finished!\n" + f"Copied {copied_count} of {len(fotos_list)}"
easygui.msgbox(msg=message)

# END

