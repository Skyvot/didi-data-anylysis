import os
import time
def run(x):
    strx = str(x)
    if x < 10:
        strx = '0'+strx
    start_time = time.time()
    inf = open('endpoint1001', 'r')
    lines = inf.readlines()
    baidu = open('data/endpoint1001baidu'+str(x), 'w')
    linedatalist = []
    for line in lines:
        linedata = line.split(',')
        linedata[2] =linedata[2].replace('\n', '')
        linedatalist.append(linedata)
    readtime = time.time()
    processing_cnt = 0
    for linedata in linedatalist:
        if time.strftime("%H", time.localtime(int(linedata[0]))) == strx:
            str_temp = '{"lat":'+linedata[2]+',"lng":'+linedata[1]+',"count":'+str(1)+'},\n'
            if 34.21 < float(linedata[2]) < 34.27 and 108.92 < float(linedata[1]) < 108.99:   # 34.20-24.28 108.91-109.00
                baidu.write(str_temp)
    process_time = time.time()
    print('reading time: '+str(readtime - start_time))
    print('processing time: '+str(process_time - readtime))
    print('total time: '+str(process_time - start_time))


if __name__ == '__main__':
    for i in range(15, 16):
        run(i)
