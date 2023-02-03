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

import argparse
import sys
import logging
from fotofiler.wizard import wizard
import fotofiler.nongui 


# MAIN
def main():
    """ The main function processing the command line arguments in argv
    """
    parser = argparse.ArgumentParser(description="Copy and archive (photo) files")
    parser.add_argument('-w','--wizard', 
                        action='store_true',
                        help='Start in wizard mode with GUI')
    parser.add_argument('-s','--source', nargs=1,
                        help='Source path where to look for files')
    parser.add_argument('-d','--destination', nargs=1,
                        help='Path to where subdirectories are created for copied files')
    parser.add_argument('-p', '--pattern', nargs=1,
                        help='Pattern to match source files. Default=*.*; could be *.jpg for example',
                        default='*.*')
    parser.add_argument('-q','--quiet',
                        action='store_true',
                        help='Quiet, get no information of progress')
    parser.add_argument('-n','--noask',
                        action='store_true',
                        help='Just run, with no unnecessary interactive questions on console, please')
    parser.add_argument('-g','--debug',
                        action='store_true',
                        help='sets logging level DEBUG, causing verbose prints to console')
    args = parser.parse_args()

    if args.debug :
        log_level='DEBUG'
    else:
        log_level = None

    logging.basicConfig(level=log_level)
    if args.wizard or len(sys.argv) == 1:
        print('No arguments, starting wizard (use -h for help about other options)')
        wizard()        
    elif args.source != None and args.destination != None:
        logging.debug(f'Source dir = {args.source}')
        logging.debug(f'Destination dir = {args.destination}')
        logging.debug('File pattern = {args.pattern}')
        logging.debug('Quiet? {args.quiet}')
        logging.debug('Not asking questions? {args.noask}')
        fotofiler.nongui.run_copy(source=args.source[0], 
                                    destination=args.destination[0], 
                                    pattern=args.pattern[0],
                                    quiet=args.quiet,
                                    dontask=args.noask)
