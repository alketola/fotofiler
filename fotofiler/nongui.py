
import os
import sys
import fotofiler.fileutil

from fotofiler.fotolist import build_fotos_list

def run_copy(source : os.PathLike, destination : os.PathLike, pattern , quiet : bool, dontask : bool):

    # # TODO: ensure that source is a directory
    source_contents = os.listdir(destination)
    source_count = len(source_contents)
    if source_count==0:
        if not quiet:
            print("No source files?")
        sys.exit()

    source_spec = os.path.join(source,'**/'+pattern) 
    if not quiet:
        print("Source_path",source_spec)

    if not quiet:
        print("Analysing... this may take a while")
    fotos_list = []

    fotos_list, dest_dir_set = build_fotos_list(None,
                                                source_spec,
                                                recurse=True,
                                                dest_root=destination)
    if not quiet:
        print("Number of files to copy:", len(fotos_list))

    dest_contents = os.listdir(destination)
    dest_count = len(dest_contents)
    if dest_count==0:
        dest_description = "is empty"
    else:
        dest_description = f"already has {len(dest_contents)} files:\n"
        for f in dest_contents:
            dest_description += f + '\n'
    if not quiet:
        print(f'The files will be copied and folders created in {destination}, which {dest_description}')
        
    message = f'\n{len(fotos_list)} files will be copied to {len(dest_dir_set)} folders' 
    message += f'\nDestination root={destination} '

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

    go_copy = True
    if dontask:
        go_copy = True
    else:
        print('Start copying y/N')
        yn = input()
        if yn != 'y':
            go_copy = False

    if not go_copy:
        sys.exit("Cancelled.")


    # Create dirs
    if not quiet:
        print("Creating folders")

    fotofiler.fileutil.make_dirs(destination, dest_dir_set, None)
    
    # Copy files
    if not quiet: 
        print("Copying")

    copied_count=0
    failed_count=0
    copied_count, failed_count = fotofiler.fileutil.copy_files(fotos_list, progress_callback=None)
    if not quiet:
        print(f"Copying Finished!\nCopied {copied_count} of {len(fotos_list)}")

# END nongui