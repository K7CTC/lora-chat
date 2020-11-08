########################################################################
#                                                                      #
#          NAME:  LoRa Chat - Create SQLite 3 Database                 #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.8                                                 #
#   DESCRIPTION:  This module creates lora_chat.db and populates it    #
#                 with data from nodes.csv                             #
#                                                                      #
########################################################################

import csv
import sqlite3
import sys
from pathlib import Path

if Path('lora_chat.db').is_file():
    print('ERROR: lora_chat.db already exists')
    sys.exit(1)

if Path('nodes.csv').is_file() == False:
    print('ERROR: File not found - nodes.csv')
    sys.exit(1)

try:
    db = sqlite3.connect('lora_chat.db')
    db.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            node_id	                        INTEGER NOT NULL UNIQUE,
            node_name	                    TEXT NOT NULL,
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
    print('FAIL!')
    sys.exit(1)
else:
    print('PASS!')
    sys.exit(0)