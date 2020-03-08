import os
import time
start_time = time.time()
inf = open('sorted1001', 'r')
lines = inf.readlines()
# resultf = open('result1001', 'w')
# sortedf = open('sorted1001', 'w')
endf = open('endpoint1001', 'w')
linedatalist = []
for line in lines:
    linedata = line.split(',')
    linedatalist.append(linedata)
readtime = time.time()
# linedatalist.sort(key=lambda x: (x[1], x[2]))
sort_time = time.time()
preid = ''
predata = []
processing_cnt = 0
for linedata in linedatalist:
    if processing_cnt%1000 == 0:
        print('Processing line '+str(processing_cnt))
    processing_cnt += 1
    # sortedf.write(linedata[0]+','+linedata[1]+','+linedata[2]+','+linedata[3]+','+linedata[4])
    if linedata[1] != preid and preid != '':
        endf.write(predata[2]+','+predata[3]+','+predata[4])
    preid = linedata[1]
    predata = linedata
process_time = time.time()
print('reading time: '+str(readtime - start_time))
print('sorting time: '+str(sort_time - readtime))
print('processing time: '+str(process_time - sort_time))
print('total time: '+str(process_time - start_time))
