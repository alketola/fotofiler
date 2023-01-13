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
from fotofiler.wizard import wizard


# MAIN
def main():
    """ The main function processing the command line arguments in argv
    """
    parser = argparse.ArgumentParser(description="Copy and archive photo files")
    parser.add_argument('--wizard', 
                        action='store_true',
                        help='Start in wizard mode with GUI')
    parser.add_argument('--source', nargs=1,
                        help='Source path where to look for files')
    parser.add_argument('--destination', nargs=1,
                        help='Path to where subdirectories are created for copied files')
    parser.add_argument('--pattern', nargs=1,
                        help='Pattern to match source files. Default=*.*; could be *.jpg for example')
    args = parser.parse_args()
    if args.wizard or len(sys.argv) == 1:
        print('Starting wizard (use -h for help about other options)')
        wizard()        
    else:
        print(args)
