__author__ = 'jparsaie'

import os
import shutil
import datetime

def get_distro_list(mainDirectory):
    service_distros = []
    revision_list = os.listdir(mainDirectory)

    for r in revision_list:
        revision_distros = os.listdir(os.path.join(mainDirectory, r))

        for rd in revision_distros:
            service_distros.append(os.path.join(r, rd))

    service_distros.sort()
    service_distros.reverse()

    return service_distros

def get_keep_discard_list(distroList, serviceDirectory):
    keep = []
    discard = []

    for i in range(0, len(distroList)):
        distro = distroList[i]
        action = "KEEP"
        if(i < 5):
            keep.append(distro)
        else:
            discard.append(distro)
            action = "DISCARD"

        log(os.path.join(serviceDirectory, distro), get_file_size(os.path.join(serviceDirectory, distro)), action)

    print '\n'
    return keep, discard

def log(serviceDirectory):
    print "Cleaning up service [" + serviceDirectory.upper() + "]..."

def log(distro, distroSize, action):
    now = datetime.datetime.now()

    with open("test.txt", "a") as testFile:
        testFile.write("[" + distro + "]" \
                       "[" + str("%.2f" % distroSize) + "mb]" \
                       "[" + action + "]"\
                       "[" + str(now.month) + '/' + str(now.day) + '/' + str(now.year) + "" \
                       " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]\n")

    print "\t[" + distro + "]" \
           "[" + str("%.2f" % distroSize) + "mb]" \
           "[" + action + "]"\
           "[" + str(now.month) + '/' + str(now.day) + '/' + str(now.year) + "" \
           " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]"

def get_file_size(fileDirectory):
    total_size = 0

    for(path, dirs, files) in os.walk(fileDirectory):
        for file in files:
            file_name = os.path.join(path, file)
            total_size += os.path.getsize(file_name)

    return total_size / (1024 * 1024.0)

if __name__ == '__main__':
    distros = get_distro_list("E:\Distro\Cicada")
    get_keep_discard_list(distros, "E:\Distro\Cicada")