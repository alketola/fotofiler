import os
import glob
import math

from fotocopy.fotoexif import get_datetime, get_y_ym_dirname_from_datetime

from fotocopy.fotoinfo import FotoInfo

def build_fotos_list(progress_win, source_dir, recurse, dest_root):
    """
    Searchs files from source dir, and create list of FotoInfo objects,
    and a list of destination folders to be created.

    >>> L, dirs = build_fotos_list("test/assets/EXIFTEST1.JPG",False,"test/assets")
    >>> len(L)
    1
    >>> len(dirs)
    1
    >>> L[0].filename
    'EXIFTEST1.JPG'
    >>> dirs.pop()
    '/2022/2022-11'
    """
    foto_list = []
    dest_dir_set = set()
    
    progress_win._progressbar.configure(mode="indeterminate")
    progress_win.set_status("Reading source directory")
    progress_win._progressbar.start()
    globlist = list(glob.iglob(source_dir, recursive=recurse))
    progress_win._progressbar.stop()
    progress_win._progressbar.configure(mode="determinate")
    progress_win.reset_progress()
    progress_win.set_status("Collecting information")
 

    
    filecount = len(globlist)
    nud = math.floor(filecount/100) + 1
    c = 0
    for filename in globlist:
        if c % nud == 0:
            progress_win.nudge()
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
        c = c + 1

    progress_win.stop_now()
    return (foto_list, dest_dir_set)
