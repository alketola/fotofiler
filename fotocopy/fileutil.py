
import os
import glob
import math
import shutil

def make_dirs(dest_root, dest_dir_set, progess_callback=None):
    """ Make directories (folders) at dest_root path, from dest_dir_set.
        Nudge progress indicator given by progress_callback, up to 100%.
    """
    
    dir_count = len(dest_dir_set)
    nud = math.floor(dir_count / 100) + 1
    counter = 0
    for d in dest_dir_set:
        if progess_callback != None:
            if counter % nud == 0:            
                progess_callback()
        try:        
            os.makedirs(dest_root+d, exist_ok=True)
        except:
            pass
        counter = counter + 1    

def copy_files(fotos_list, progress_callback=None):
    copied_count=0
    failed_count=0
    foto_count = len(fotos_list)
    nud = math.floor(foto_count / 100) + 1
    for f in fotos_list:
        if progress_callback != None:
            if copied_count % nud == 0:
                progress_callback()
        try :
                shutil.copy2(f.source_path,f.full_dest_path)
                copied_count = copied_count + 1
        except Exception as e:
            failed_count = failed_count + 1
            print(f'A copy failed because {e}',end='\n')
            
        if (copied_count+failed_count) % 79 == 0 :
            print(f'     \r{copied_count}\r', end='', flush=True)
    print(f'Copied: {copied_count} failed: {failed_count}')
    return copied_count, failed_count