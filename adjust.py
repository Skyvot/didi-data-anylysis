import os
import time
def run(x):
    strx = str(x)
    if x < 10:
        strx = '0'+strx
    inf = open('result1001', 'r')
    lines = inf.readlines()
    baidu = open('data/adjusted_startpoint1001baidu'+str(x), 'w')
    linedatalist = []
    for line in lines:
        linedata = line.split(',')
        linedata[2] =linedata[2].replace('\n', '')
        linedatalist.append(linedata)
    point_dict = {}
    for linedata in linedatalist:
        if time.strftime("%H", time.localtime(int(linedata[0]))) == strx:
            linedata[1] = str(round(float(linedata[1]), 3))
            linedata[2] = str(round(float(linedata[2]), 3))
            hash_point = str(linedata[1])+','+str(linedata[2])
            if hash_point in point_dict.keys():
                point_dict[hash_point] = point_dict[hash_point]+1
            else:
                point_dict[hash_point] = 1
    for key in point_dict.keys():
        point_data = key.split(',')
        str_temp =point_data[1]+','+point_data[0]+','+str(point_dict[key])+'\n'
        baidu.write(str_temp)


if __name__ == '__main__':
    for i in range(0, 24):
        run(i)
