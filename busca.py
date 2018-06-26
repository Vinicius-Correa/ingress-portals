#!/usr/bin/env python

import re, os.path

filename = 'base'
flag = False

if (os.path.isfile(filename + ".txt") == True):
    file_csv = open(filename + "-draw.txt", "w")
    file_table = open(filename + "-table.csv", "w")
    searchfile = open(filename + ".txt", "r")

    file_csv.write('[')
    file_table.write('Portal,Latitude,Longitude,Discovered\n')
    for line in searchfile:
        if "Portal: " in line:
            #portal=line.split(": ")[1]
            portal=line[line.find("Portal: ")+8:line.find("\n")]
            file_table.write(portal + ",")
        if "intel?ll" in line:
            lat=line[line.find("intel?ll=")+9:line.find(",")]
            long=line[line.find(",")+1:line.find("&z=15&pll")]
            if (flag == True):
                file_csv.write(',')
            else:
                flag = True
            file_csv.write('{"type":"marker","latLng":{"lat":')
            file_csv.write(lat + ',"lng":' + long)
            file_csv.write('},"color":"#ff0000"}')
            file_table.write(lat + "," + long + ",")
        if "Discovered by" in line:
            discov=line.split(": ")[1]
            file_table.write(discov)
    file_csv.write(']')
    searchfile.close()
    file_csv.close()
    print ("Files generated.")
else:
    print ("Error: File " + filename + ".txt not found.")
