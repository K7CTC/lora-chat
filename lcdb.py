########################################################################
#                                                                      #
#          NAME:  LoRa Chat - Database Functions                       #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.1                                                 #
#   DESCRIPTION:  This module contains database functions for LoRa     #
#                 Chat and is only intended for import into other      #
#                 project modules.  Not to be executed directly!       #
#                                                                      #
########################################################################

import csv
import os
import sqlite3
import sys
from pathlib import Path

#function: clear terminal
def clear_terminal():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

#function: check for database and create if it doesn't exist
# returns: boolean
def exists():
    if Path('lora_chat.db').is_file():
        return True
    else:
        if Path('nodes.csv').is_file() == False:
            print('ERROR: File not found - nodes.csv')
            print('HELP: nodes.csv is required for database creation.')
            return False
        try:
            db = sqlite3.connect('lora_chat.db')
            db.execute('''
                CREATE TABLE IF NOT EXISTS nodes (
                    node_id	                        INTEGER NOT NULL UNIQUE,
                    node_name	                    TEXT NOT NULL,
                    my_node                         TEXT UNIQUE,
                    PRIMARY KEY(node_id));''')
            db.execute('''
                CREATE TABLE IF NOT EXISTS sms (
                    node_id                         INTEGER NOT NULL,
                    message	                        TEXT NOT NULL,
                    payload_raw                     TEXT NOT NULL,
                    payload_hex                     TEXT NOT NULL,
                    time_queued	                    INTEGER,
                    time_sent	                    INTEGER,
                    air_time	                    INTEGER,
                    time_received	                INTEGER,
                    rssi                            INTEGER,
                    snr                             INTEGER,
                    FOREIGN KEY (node_id) REFERENCES nodes (node_id));''')
            db.commit()
            with open('nodes.csv') as csvfile:
                nodes = csv.DictReader(csvfile)
                to_db = [(i['node_id'],
                        i['node_name'])
                        for i in nodes]
            db.executemany('''
                INSERT INTO nodes (
                    node_id,
                    node_name)
                VALUES (?, ?);''', to_db)
            db.commit()
            db.close()
        except:
            db.close()
            print('ERROR: Unable to create lora_chat.db!')
            return False
        else:
            return True

#function: obtain number of rows in nodes table
# returns: row count as integer
def nodes_row_count():
    db = sqlite3.connect('lora_chat.db')
    row_count = db.execute('SELECT COUNT(*) FROM nodes').fetchone()[0]
    db.close()
    return row_count    

#function: logic to obtain and set the my_node boolean value
# returns: my_node_id integer or None
def my_node_id():
    db = sqlite3.connect('lora_chat.db')
    c = db.cursor()
    c.execute('SELECT node_id FROM nodes WHERE my_node = "True"')
    my_node_id = c.fetchone()
    if my_node_id != None:
        c.close()
        db.close()
        return my_node_id[0]
    max_node_id = nodes_row_count()
    clear_terminal()
    print('┌─┤Set My Node ID├─────────────────────────────────────────────────┐')
    print('│ Please choose your node identifier from one of the following:    │')
    c.execute('''
        SELECT
            node_id,
            node_name
        FROM
            nodes;''')
    for record in c.fetchall():
        node_id = record[0]
        node_name = record[1]
        print(f'│     {node_id} - {node_name}')
    print('└──────────────────────────────────────────────────────────────────┘')
    my_node_id = input('Choose (1-' + str(max_node_id) + '): ')
    try:
        my_node_id = int(my_node_id)
    except:
        print(f'HELP: Node identifier must be an integer between 1 and {str(max_node_id)}!')
        return None
    if my_node_id < 1 or my_node_id > max_node_id:
        print(f'HELP: Node identifier must be an integer between 1 and {str(max_node_id)}!')
        return None
    c.execute('''
        UPDATE
            nodes
        SET
            my_node=?
        WHERE
            node_id=?;''',
        ("True", my_node_id))
    db.commit()
    c.execute('SELECT node_id FROM nodes WHERE my_node = "True"')
    my_node_id = c.fetchone()
    if my_node_id != None:
        return my_node_id[0]
    else:
        return None
        
        
#function: logic to obtain and set the my_node boolean value
# returns: boolean
def set_my_node_id():
    db = sqlite3.connect('lora_chat.db')
    c = db.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    c.execute('''
        UPDATE
            nodes
        SET
            time_sent=?,
            air_time=?
        WHERE
            rowid=?;''',
        (time_sent,air_time,rowid))
    db.commit()

    print('ERROR: Unable to update database record of transmitted message!')
    logging.error('Unable to update database record of transmitted message!')
    sys.exit(1)



#function: check for configuration file and create if it doesn't exist
# accepts: max node id integer
# returns: boolean
def config_exists(max_node_id):
    if Path('lora_chat.conf').is_file():
        return True
