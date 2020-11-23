########################################################################
#                                                                      #
#          NAME:  LoRa Chat - New SMS                                  #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.9                                                 #
#   DESCRIPTION:  This module reads lora_chat.conf to obtain the node  #
#                 identifier and validates a user provided message of  #
#                 up to 50 characters. An SMS packet type identifier   #
#                 is appended and the resulting data is inserted into  #
#                 a new row within the sms table of lora_chat.db.      #
#                                                                      #
########################################################################

#import from project library
import lc
import lcdb

#import from standard library
import argparse
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

#establish and parse command line arguments
parser = argparse.ArgumentParser(description='LoRa Chat - New SMS',
                                 epilog='Created by K7CTC. This module reads lora_chat.conf to '
                                        'obtain the node identifier and validates a user provided '
                                        'message of up to 50 characters. An SMS packet type '
                                        'identifier is appended and the resulting data is '
                                        'inserted into a new row within the sms table of '
                                        'lora_chat.db.')
parser.add_argument('-m', '--message', nargs='?', default=None,
                    help='message of up to 50 characters in length to be queued for transmission')
args = parser.parse_args()

if lcdb.exists() == False:
    print('ERROR: File not found - lora_chat.db')
    sys.exit(1)

my_node_id = lcdb.my_node_id()
if my_node_id == None:
    print('ERROR: Unable to set node ID for this node!')
    sys.exit(1)

my_node_name = lcdb.my_node_name(my_node_id)

#function: message validation, returns boolean
def validate_message(message_to_be_validated):
    #only contain A-Z a-z 0-9 . ? ! and between 1 and 50 chars in length
    if re.fullmatch('^[a-zA-Z0-9!?. ]{1,50}$', message_to_be_validated):
        return True
    else:
        return False

#function: insert message into database, returns boolean  
def database_entry(message):
    #compose raw packet to be sent over the air
    payload_raw = str(1) + ',' + str(my_node_id) + ',' + message
    #compose hex encoded version of raw packet to be sent over the air
    payload_hex = payload_raw.encode('UTF-8').hex()
    #attempt database entry
    try:
        db = sqlite3.connect('lora_chat.db')
        c = db.cursor()
        #enable foreign key constraints
        c.execute('PRAGMA foreign_keys = ON')
        time_queued = int(round(time.time()*1000))
        c.execute('''
            INSERT INTO sms (
                node_id,
                message,
                payload_raw,
                payload_hex,
                time_queued)
            VALUES (?, ?, ?, ?, ?);''',
            (my_node_id, message, payload_raw, payload_hex, time_queued))
    except:
        c.close()
        db.close()
        return False
    else:
        db.commit()
        c.close()
        db.close()
        return True

#function: clear terminal
def clear_terminal():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

#if message provided via command line is valid then insert into database
if args.message != None:
    if validate_message(args.message):
        #message is valid, insert into database then quit
        if database_entry(args.message):
            print('SUCCESS: Message has been queued for transmission.')
            sys.exit(0)
        else:
            print('ERROR: Database entry failure!')
            sys.exit(1)
    else:
        print('ERROR: Your message contained invalid characters or is of invalid length!')
        sys.exit(1)

#new sms loop
if args.message == None:
    while True:
        try:
            clear_terminal()
            print('┌───────────┤Experimental LoRa Mesh Messenger - New SMS├───────────┐')
            print('│ Type a message between 1 and 50 characters then press enter.     │')
            print('│ Your message may only contain A-Z a-Z 0-9 and the following      │')
            print('│ special characters: period, question mark and exclamation mark   │')
            print('└──────────────────────────────────────────────────────────────────┘')
            message = input(my_node_name + ': ')
            if validate_message(message):
                if database_entry(message):
                    print()
                    print('SUCCESS: Message has been queued for transmission.')
                    time.sleep(5)
            else:
                print()
                print('ERROR: Your message contained invalid characters or is of invalid length!')
                time.sleep(5)
        except KeyboardInterrupt:
            print()
            sys.exit(0)