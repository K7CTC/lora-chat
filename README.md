# LoRa Chat

LoRa Chat is an experimental SMS (Short Message Service) application that utilizes the LoRa modulation scheme to send and receive undirected messages of 50 characters or less.  The application is 100% scratch built in Python 3 and is writted to be cross-platform.  LoRa Chat has been tested on macOS Big Sur, Windows 10 as well as Raspberry Pi OS.  All modules have been tested with Python v3.7.3 and Python v3.9.  

## Required Hardware

* [Ronoth LoStik](https://ronoth.com/products/lostik)

## Recommended Hardware

* [915Mhz Dipole Antenna](https://lowpowerlab.com/shop/product/193)
* [915Mhz Base Antenna](https://diamondantenna.net/bc920.html)

## Required Software

* [Python 3](https://www.python.org/downloads/)
* [pySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html#installation)

## Proect File Descriptions

### lcdb.py

This module contains functions that can be called against lora_chat.db, the database that stores all application data.  These functions provide the following utility to other modules in the application:

* Check to see if lora_chat.db exists and create a new lora_chat.db if it doesn't.
  * If lora_chat.db does not exist, user will be prompted to specify their node identifier upon database creation.
* Obtain the number of nodes recognized by te application.
* Obtain the node identifer of the current (your) node.
* Obtain the node name of the current (your) node.
* Store outbound messages.
* Clear the chat history.

### lostik-service.py

This module contains all of the logic for interfacing with the Ronoth LoStik.

### nodes.csv

This comma separated values file contains a header row specifying the field names for the node table of the LoRa Chat database.  Remaining rows list the node identifier (integer between 1 and 99) along with the node name.  This file is read by the lcdb.py function when called and lora_chat.db is not found prompting the application to create a new database.  The contents of nodes.csv are populated into a database table named "nodes" for use elsewhere within the application.

### requirements.txt

This file is used by the pip package manager to install application dependencies.  Currently the only dependency is pySerial v1.5 or above.

### sms_clear.py

This module simply drops and recreates the sms table from lora_chat.db thus purging chat history.

### sms_new.py

This module validates a user provided message of up to 50 characters.  An SMS packet type identifier is appended and the resulting data is inserted into a new row within the sms table of lora_chat.db.  This module can be run interactively or non-interactively by passing the optional --msg command line argument.  If the message is passed via command line, the module will deposit the message into the database, report success/fail and exit.  If run interactively, the module will loop a prompt to provide an outgoing message.

### sms_view.py

This module reads the sms table from lora_chat.db and prints the output to the console.

### lostik.log

This file is created (and subsequently appended) by the lostik-service.py Python module.  As one would guess, it contains an event log for the service.

### lora_chat.db

This SQLite 3 database file is created automatically if not found during application execution and contains all application data.  The database contains two tables; nodes and sms.  The nodes table contains node_id (as the primary key) as well as node_name and my_node.  My_node serves to hold a boolean of true on one row to indicate your chosen node identifier.  The sms table contains; node_id (foreign key), message, payload_raw, payload_hex, time_queued, time_sent, air_time, time_received, rssi, snr.  These fields provide all that is needed to accurately record all incoming and outgoing messages.

## Quick Start

You will want to open three separate terminal windows.  Start by running sms_new.py which will trigger the creation of lora_chat.db.  On first launch, you will be prompted to select your node identififier from a list.  Please choose carefully as this setting is permanent.  If you choose incorrectly, you will need to delete lora_chat.db and start over.  In separate terminal windows, run sms_view.py and lostik-service.py.  It doesn't matter what order any of these three modules are executed as they operate asynchronously.

To send a message, simply type a message in SMS New.  Your message will be queued for transmission.  On the next transmit cycle of the LoStik, the LoStik Service checks for outgoing message(s) and transmits it.  Only one message is sent per transmit cycle using FIFO (first in, first out).  After an outgoing message has been transmitted, the database record is updated to reflect the time sent as well as the time spend "on air".  

SMS View checks for changes in the database once per second.  When an outgoing message had been sent or an incoming message has been received, it is formatted and displayed in a "chat" style interface with all pertinent details.

The LoStik Service runs in an infinite loop based on the hardware Watchdog Timer Time-Out on the LoStik or receipt of a message from another node.  The default is 8 seconds, meaning that if nothing is received within 8 seconds, the device drops out of its receive state and returns to idle.  The same is true for transmit.  A transmission longer than 8 seconds will cause the device to drop out of the transmit state and return to idle (with an error).  Upon successful message receipt the application will store the message in the database and check for the next outgoing message.  If a message is found it is sent.

## Developed By

* **Chris Clement (K7CTC)** - [https://qrz.com/db/K7CTC](https://qrz.com/db/K7CTC)
