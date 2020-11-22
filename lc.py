import csv
import sqlite3
from pathlib import Path

#function: check for database and create if it doesn't exist
# returns: boolean
def database_exists():
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
            print('ERROR: Unable to create lora_chat.db!')
            return False
        else:
            return True

#function: obtain number of rows in nodes table
# returns: row count as integer
def get_nodes_rows():
    try:
        db = sqlite3.connect('lora_chat.db')
        db.execute('''
        SELECT
            COUNT(*)
        FROM
            nodes;''')
        

        db.close()
    except:
        print('ERROR: Unable to create lora_chat.db!')
        return False
    else:
        return True





#function: check for configuration file and create if it doesn't exist
# accepts: max node id integer
# returns: boolean
def config_exists(max_node_id):
    if Path('lora_chat.conf').is_file():
        return True
    else:

