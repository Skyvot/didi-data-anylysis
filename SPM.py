from rtree import index
import os
import time
import math
s_idx = index.Index()
e_idx = index.Index()

s_point_list = []   # save point in form "[x, y, weight, num, type]"
e_point_list = []

pair_list = []  # save in form "[O_num, P_num, weight]"
satisfied = {}  # whether this O point is satisfied or not

chain = []
no_car = 0


def get_input(start_path, end_path):
    with open(start_path, 'r') as startf:
        s_lines = startf.readlines()
        num = 0
        for s_line in s_lines:
            s_linedata = s_line.split(',')
            s_linedata.append(str(num))
            s_linedata.append('start')
            num = num + 1
            s_linedata[2] = s_linedata[2].replace('\n', '')
            s_point_list.append(s_linedata)
            satisfied[s_linedata[3]] = 0
    with open(end_path, 'r') as endf:
        e_lines = endf.readlines()
        num = 0
        for e_line in e_lines:
            e_linedata = e_line.split(',')
            e_linedata.append(str(num))
            e_linedata.append('end')
            num = num + 1
            e_linedata[2] = e_linedata[2].replace('\n', '')
            e_point_list.append(e_linedata)


def idx_build():
    for s_point in s_point_list:
        s_idx.insert(int(s_point[3]), (float(s_point[0]), float(s_point[1]), float(s_point[0]), float(s_point[1])))
    for e_point in e_point_list:
        e_idx.insert(int(e_point[3]), (float(e_point[0]), float(e_point[1]), float(e_point[0]), float(e_point[1])))


def find_nne(x):
    global no_car
    nn_list = e_idx.nearest((float(x[0]),float(x[1]),float(x[0]),float(x[1])), 1)
    y = -1
    for i in nn_list:
        y = i
        break
    if y == -1:
        no_car = 1
        return []
    return e_point_list[y]


def find_nns(x):
    global no_car
    nn_list = s_idx.nearest((float(x[0]), float(x[1]), float(x[0]), float(x[1])), 1)
    y = -1
    for i in nn_list:
        y = i
        break
    if y == -1:
        no_car = 1
        return []
    return s_point_list[y]


def solve():
    for s_point in s_point_list:
        if no_car == 1:
            break
        chain.clear()
        if satisfied[s_point[3]] == 0:
            chain.append(s_point)
            while len(chain) != 0:
                x = chain[-1]
                if x[4] == 'start':
                    y = find_nne(x)
                    if no_car == 1:
                        break
                    if len(chain) == 1:
                        chain.append(y)
                        continue
                    if chain[-2] == y:
                        if int(x[2]) > int(y[2]):     # s > e
                            skey = x[0]+','+x[1]
                            ekey = y[0]+','+y[1]
                            pair_list.append('from ' + ekey + ' to ' + skey + ' ' + y[2] + ' cars.')
                            s_point_list[int(x[3])][2] = str(int(x[2]) - int(y[2]))
                            e_point_list[int(y[3])][2] = str(0)
                            # x[2] = str(int(x[2]) - int(y[2]))
                            # y[2] = str(0)
                            e_idx.delete(int(y[3]),(float(y[0]),float(y[1]),float(y[0]),float(y[1])))
                            chain.pop(-1)
                            chain.pop(-1)
                        else:   # s < e
                            skey = x[0] + ',' + x[1]
                            ekey = y[0] + ',' + y[1]
                            pair_list.append('from ' + ekey + ' to ' + skey + ' ' + x[2] + ' cars.')
                            e_point_list[int(y[3])][2] = str(int(y[2])-int(x[2]))
                            s_point_list[int(x[3])][2] = str(0)
                            # y[2] = str(int(y[2])-int(x[2]))
                            # x[2] = str(0)
                            satisfied[x[3]] = 1
                            s_idx.delete(int(x[3]),(float(x[0]),float(x[1]),float(x[0]),float(x[1])))
                            chain.pop(-1)
                            if e_point_list[int(y[3])][2] == '0':
                                e_idx.delete(int(y[3]), (float(y[0]), float(y[1]), float(y[0]), float(y[1])))
                                chain.pop(-1)
                    else:
                        chain.append(y)
                else:
                    y = find_nns(x)     # x is end, y is start
                    if no_car == 1:
                        break
                    if len(chain) == 1:
                        chain.append(y)
                        continue
                    if chain[-2] == y:
                        if int(x[2]) < int(y[2]):  # s > e  y > x
                            skey = y[0] + ',' + y[1]
                            ekey = x[0] + ',' + x[1]
                            pair_list.append('from ' + ekey + ' to ' + skey + ' ' + x[2] + ' cars.')
                            s_point_list[int(y[3])][2] = str(int(y[2]) - int(x[2]))
                            e_point_list[int(x[3])][2] = str(0)
                            # y[2] = str(int(y[2]) - int(x[2]))
                            # x[2] = str(0)
                            e_idx.delete(int(x[3]), (float(x[0]), float(x[1]), float(x[0]), float(x[1])))
                            chain.pop(-1)
                            if s_point_list[int(y[3])][2] == '0':
                                chain.pop(-1)
                                satisfied[y[3]] = 1
                                s_idx.delete(int(y[3]), (float(y[0]), float(y[1]), float(y[0]), float(y[1])))
                        else:  # s < e  y < x
                            skey = y[0] + ',' + y[1]
                            ekey = x[0] + ',' + x[1]
                            pair_list.append('from ' + ekey + ' to ' + skey + ' ' + y[2] + ' cars.')
                            e_point_list[int(x[3])][2] = str(int(x[2]) - int(y[2]))
                            e_point_list[int(y[3])][2] = str(0)
                            # x[2] = str(int(x[2]) - int(y[2]))
                            # y[2] = str(0)
                            satisfied[y[3]] = 1
                            s_idx.delete(int(y[3]), (float(y[0]), float(y[1]), float(y[0]), float(y[1])))
                            chain.pop(-1)
                            chain.pop(-1)
                    else:
                        chain.append(y)
        else:
            continue


def output():
    outputf = open('output/SPM_result100115', 'w')
    for line in pair_list:
        outputf.write(line+'\n')


def main():
    get_input('data/adjusted_startpoint1001baidu15', 'data/adjusted_endpoint1001baidu15')
    st = time.time()
    idx_build()
    solve()
    output()
    runtime = time.time()-st
    print(runtime)


if __name__ == '__main__':
    main()
