#!/usr/bin/env python3

''' Read a single CSV file which stores metadata for storage into mysql database tables,
        outputs the mysql commands to insert all metadata (eg. redirect to file).
    Store data for all the tables in one pass by making assumptions about structure of data.
    Assume: if only column 1 (0 based) is populated, then it is the name of a table,
            check this with a list of tables in the database.
    Assume: If column 0 is populated, then it is not a row of data.
    Assume: 1st 2 columns after a "table name" column are the header, which include the
            db column names - use this to form the INSERT command.
SAMPLE DATA------------------------------------------------            
,node_config,,,,,,,,,,,,
,node_config_id,name,node_id,time_started,street_address,location_lat,location_long,location_altitude,location_elevation,location_orientation,config, time_created,time_last_updated
,INT,TEXT,VARCHAR(32),TIMESTAMP,TEXT,FLOAT,FLOAT,FLOAT,FLOAT,FLOAT,JSON,TIMESTAMP,TIMESTAMP
,,003,0000001E0610893C,,Halsted St & Randolph St,41.884541,-87.647416,,,NEC,,,
,,00B,0000001E061089C0,,Wood St & Warren Blvd,41.882331,-87.671736,,,NEC,,,
,,00C,0000001E06108081,,Kedzie Ave & 5th Ave,41.878394,-87.70602,,,NEC,,,
,,00D,0000001E0610890A,,,,,,,,,,
,,010,0000001E06107C9E,,,,,,,,,,
,,011,0000001E061089FA,,Damen Ave & Archer Ave,41.831792,-87.675331,,,SEC,,,
,,012,0000001E06107FF0,,Damen Ave & Cermak Rd,41.852161,-87.675846,,,SEC,,,
,,014,0000001E06107E5D,,State St & Washington St,41.883214,-87.627869,,,SEC,,,
--------------------------------------------------------------            
'''

import csv
import sys

if __name__ == '__main__':
    bVerbose = len(sys.argv) > 1 and sys.argv[1] == '-v'
    
    if bVerbose: print('#' * 100 + '\n')
    with open('/media/sf_share/UrbanCCD/AoT MetaData - Crowdsourced - Sheet1.csv', 'r') as fIn:
        csvReader = csv.reader(fIn)
        tableName = None
        headers = None
        for iRow, rowRaw in enumerate(csvReader):
            row = [x.strip() if x != '' else None for x in rowRaw]  # clean entries
            fullColumns = [iCol for iCol, col in enumerate(row) if col is not None]
            if bVerbose: print(iRow, row, fullColumns)

            if len(fullColumns) == 0 or 0 in fullColumns:    # we left the table
                tableName = None
                headers = None
            elif fullColumns == [1]:  # table title
                if bVerbose: print('NEW TABLE*****************')
                iRowTable = iRow
                tableName = row[1]
                headers = None
                print('TRUNCATE TABLE {};'.format(tableName))
            elif iRow == iRowTable + 1:     # get the headers
                headers = row
                nColumns = len(headers)
            elif iRow == iRowTable + 2:     # skip
                pass
            else:   # column 1 or greater is full
                if headers and tableName:
                    if bVerbose: print('headers:', headers)
                    if bVerbose: print('fullColumns:', fullColumns)
                    columnElements = list()
                    valueElements = list()
                    for i in range(len(headers)):
                        if headers[i] and row[i]:
                            columnElements.append(headers[i])
                            valueElements.append('"' + row[i] + '"')
                    cmd = 'INSERT INTO waggle.{} ({}) VALUES ({});'.format(tableName,
                        ', '.join(columnElements), 
                        ', '.join(valueElements))
                    print(cmd)
                else:
                    print('ERROR: data appears without tableName or headers:',
                        '\n row #', iRow, 
                        '\n tableName:', tableName,
                        '\n headers:', headers)
                    break
                