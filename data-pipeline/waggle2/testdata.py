#!/usr/bin/python3
''' Generates test data in the CSV (with header) format that simulates the extracted from sensor database table2/db_decoded.
'''
import datetime
import json
import math

""" SAMPLE DATA (from old syntax)

HEADERS:
node_id, ingest_id, meta_id, timestamp, data_set, sensor, parameter, value, unit

DATA (OLD format):
0000001e06107ff0;2016-09-13;base plugin;1;default;2016-09-13 00:00:09.385000;wagman_info;meta.txt;[':', 'id:00403AB000D3A582', 'hbeat_nc:3/6', 'enabled:1 1 1 0 0', 'env:35.39 26.01', 'date:2016 9 13 0 2 49', 'hbeat_cs:4/6', 'nc_info:current normalcurrent normal', 'fails:0 0 0 0 0', 'media:sd sd', 'cu:160 192 176 160 112 128', 'gn_info:current normalcurrent normalcurrent normal', 'hbeat_gn:3/6', 'th:759 665 670 672 707']

NOTE: the timestamp is the integer number of milliseconds after the epoch
"""
if True:    # this "if" suggests various configurations are possible
    filenameParameters = 'testparameters.json'
    filenameData   = 'testdata.csv'
    sampleScale = 1.03      # scale normalized signal by >1 to cause out-of-range error
    NUM_SAMPLES = 11
    nodes = ['node0']
    # Each sensor description is a dictionary of parameter descriptions.  
    # Each parameter description is a dictionary of 'units', 'minValue', etc.
    parameters = [
        {
            'sensor' : 'sensor0',
            'parameter' : 'temp',
            'unit' : 'degrees C',
            'minValue' : 0,
            'maxValue' : 100,
            'precision' : 0.1,
            'datasheet' : 'www.google.com',
            'url' : 'www.bing.com'
        },
        {
            'sensor' : 'sensor1',
            'parameter' : 'temp',
            'unit' : 'degrees C',
            'minValue' : -4,
            'maxValue' : 105,
            'precision' : 0.5,
            'datasheet' : 'www.google.com',
            'url' : 'www.bing.com'
        },
        {
            'sensor' : 'sensor1',
            'parameter' : 'hum',
            'unit' : 'percent',
            'minValue' : 0,
            'maxValue' : 100,
            'precision' : 1,
            'datasheet' : 'www.google.com',
            'url' : 'www.bing.com'
        }
    ]
###############################################################################
if __name__ == "__main__":
    t0 = datetime.datetime.now()                # simulated time of first sample
    dt = datetime.timedelta(seconds = 1)        # simulated time between samples

    with open(filenameData, 'w') as fOut:
        fOut.write('node_id,ingest_id,meta_id,timestamp,data_set,sensor,parameter,value,unit')   # first line is header
        idxSignal = 0
        bFirst = True
        for node in nodes:
            for p in parameters:
                idxSignal += 1     # each sensor generates a signal, indexed by this
                xMin = p['minValue']
                xMax = p['maxValue']
                precision = p['precision']
                frequency = 2.0 * math.pi * idxSignal / (NUM_SAMPLES - 1)
                x0 = 0.5 * (xMax + xMin)
                xAmplitude = 0.5 * sampleScale * (xMax - xMin)
                print("sensor = {}, param = {}, min = {}, max = {}, precision = {}".format(
                    p['sensor'], p['parameter'], xMin, xMax, p['precision']))
                t = t0                     # simulated time of first sample
                for idxSample in range(NUM_SAMPLES):
                   
                    x = x0 + xAmplitude * math.sin(frequency * idxSample)
                    x = precision * math.floor(x / precision + 0.5)
                    if bFirst:  # all lines but the 1st get the comma before them
                        bFirst = False
                        fOut.write('\n')
                    else:
                        fOut.write(',\n')
                    s = '{node_id},{ingest_id},{meta_id},{timestamp},{data_set},{sensor},{parameter},{value},{unit}'.format(
                        node_id = node,
                        ingest_id = idxSample,
                        meta_id = 0,
                        timestamp = int(t.timestamp() * 1000),
                        data_set = 0,
                        sensor = p['sensor'],
                        parameter = p['parameter'],
                        value = x,
                        unit = p['unit']
                    )
                    fOut.write(s)
                    print(idxSignal, idxSample, x)
                    t += dt
       
    # write out parameters
    with open(filenameParameters, 'w') as fOut:
        s = json.dumps(parameters, indent = 4)
        fOut.write(s + '\n')       
