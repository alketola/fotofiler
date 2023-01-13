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
from fotocopy.wizard import wizard


# MAIN
def main():
    """ The main function processing the command line arguments in argv
    """
    parser = argparse.ArgumentParser(description="Copy and archive photo files")
    parser.add_argument('--wizard', 
                        action='store_true',
                        help='Start in wizard mode with GUI')

    args = parser.parse_args()
    if args.wizard or len(sys.argv) == 1:
        print('Starting wizard (use -h for help about other options)')
        wizard()        
    else:
        print(args)
