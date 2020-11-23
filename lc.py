########################################################################
#                                                                      #
#          NAME:  LoRa Chat - Functions                                #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.25                                                #
#   DESCRIPTION:  This module contains functions for LoRa Chat and is  #
#                 only intended for import into other project modules. #
#                 Not to be executed directly!                         #
#                                                                      #
########################################################################

import os
import sys

#this module should not be executed directly
if __name__ == '__main__':
    print('ERROR: lc.py is not intended for direct execution!')

#function: clear terminal
def clear_terminal():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')