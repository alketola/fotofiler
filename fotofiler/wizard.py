# Photo collection reordering wizard
#
# By Antti Ketola, 2022
# In Colmenar VIejo, Spain
#
# 1. Ask to select source folder
# 2. Find files
#       Find dates
# 3. Calculate new paths and filenames
# 4. Ask to select destination folder
# 5. Create destination tree
# 6. Preview. OK=> continue, NOK=> Back
# 7. Create command queue
# 8. Display progress bar
# 9. Execute commands

import os
#import shutil
import tkinter as tk
import easygui
import pprint
from pprint import pprint

import fotofiler.fotoinfo
from fotofiler.fotoinfo import FotoInfo
import fotofiler.fotoexif
from fotofiler.fotoexif import *
import fotofiler.progress_window
from fotofiler.progress_window import *
from fotofiler.fotolist import build_fotos_list
import fotofiler.fileutil

def wizard():
    """ THE INTERACTIVE WIZARD HERE
    """
    welcome_msg="""Welcome to copy photo and other files!

                   All files are copied, from the selected source.
                   The files are then arranged to a tree, according to
                   date.

                   The program makes folders of years,
                   and inside them, there will be subfolders
                   for each month

                   Photos with EXIF data will have some analysis.
                   The photo file date is deduced from:
                   1. EXIF DateTimeOriginal
                   2. EXIF other DateTime
                   3. File modification or creation time, whichever older
                   4. File name

                   Other files go with the older filesystem date.

                """
    easygui.msgbox(welcome_msg,"fotofiler by Antti Ketola 2022 version {version}")

    # Ask source folder, from where files are copied
    source_dir = easygui.diropenbox(title="Please input source folder of photos")
    if source_dir is None:
        sys.exit("No source folder selected, exiting")
    else:
        print("Source dir",source_dir)

    source_spec = os.path.join(source_dir,'**/*.*') 
    print("Source_path",source_spec)

    # Ask destination folder, where files are copied to
    dest_root = easygui.diropenbox(title="Please input destination folder of photos",
                                       default="C:/")

    if dest_root is None:
        sys.exit("No destination folder selected, exiting")
    else:
        print("Destination folder",dest_root)

    print("Analysing... this may take a while")

    bwin = progress_window()

    fotos_list = []

    fotos_list, dest_dir_set = build_fotos_list(bwin,
                                                source_spec,
                                                recurse=True,
                                                dest_root=dest_root)
        
    print("Number of files to copy:", len(fotos_list))
    dest_contents = os.listdir(dest_root)
    dest_count = len(dest_contents)
    if dest_count==0:
        dest_description = "is empty"
    else:
        dest_description = f"already has {len(dest_contents)} files:\n"
        for f in dest_contents:
            dest_description += f + '\n'
    print(f'The files will be copied and folders created in {dest_root}, which {dest_description}')

    title = 'Start copying?'
    message = f'\n{len(fotos_list)} files will be copied to {len(dest_dir_set)} folders' 
    message += f'\nDestination root={dest_root} '

    max_shown = 10
    if dest_count > 0:
        message += "isn't empty \nThere are the following files or folders:\n"
        for f in dest_contents[:max_shown]:
            message += f"\t{f}\n"
        if dest_count > max_shown:
            message += "\t...and there's more \n"

    message += f"{len(dest_dir_set)} subfolders will be created (if non-existent):\n"
    for d in list(dest_dir_set)[:10]:
        message += "\t"+d+'\n'

    if len(dest_dir_set)>max_shown:
        message += "\t...and more"

    go_copy = easygui.ccbox(message, title)

    if not go_copy:        
        sys.exit("Cancelled.")

    # Create new Tkinter window for progress info
    pwin = progress_window()


    # Create dirs
    print("Creating folders")
    pwin.set_status("Creating folders");
##    dir_count = len(dest_dir_set)
##    nud = math.floor(dir_count / 100) + 1
##    counter = 0
##    for d in dest_dir_set:
##        if counter % nud == 0:
##            pwin.nudge()
##        os.makedirs(dest_root+d, exist_ok=True)
##        counter = counter + 1
    fotofiler.fileutil.make_dirs(dest_root, dest_dir_set, pwin.nudge)
    
    pwin.reset_progress()

    # Copy files
    print("Copying")
    pwin.set_status("Copying files")
    copied_count=0
    failed_count=0
##    foto_count = len(fotos_list)
##    nud = math.floor(foto_count / 100) + 1
##    for f in fotos_list:
##        if copied_count % nud == 0:
##            pwin.nudge()
##        try :
##                shutil.copy2(f.source_path,f.full_dest_path)
##                copied_count = copied_count + 1                
##        except Exception as e:
##            failed_count = failed_count + 1
##            print('E',end='')
##            
##        if (copied_count+failed_count) % 79 == 0 :
##            print("",flush=True)
    copied_count, failed_count = fotofiler.fileutil.copy_files(fotos_list, progress_callback=pwin.nudge)
    pwin.stop_now()

    message = "Copying Finished!\n" + f"Copied {copied_count} of {len(fotos_list)}"
    message += "\n\n\tClick OK to exit"
    easygui.msgbox(msg=message)

# END WIZARD
