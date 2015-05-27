__author__ = 'jparsaie'

import os
import shutil
import datetime

#Provided a directory to a service, gather all subdirectories for all
#distros in all of the revisions for the service. Return that list.
def get_distro_list(serviceDirectory):
    service_distros = []
    revision_list = os.listdir(serviceDirectory)

    #Iterate through revisions in service. Store all distros in all
    #revisions into service_distros.
    for r in revision_list:
        revision_distros = os.listdir(os.path.join(serviceDirectory, r))

        for rd in revision_distros:
            service_distros.append(os.path.join(r, rd))

    ##Sort and reverse the list for proper analysis in get_keep_discard_list()
    service_distros.sort()
    service_distros.reverse()

    return service_distros

#Provided a list of all distros in a service, return a list of
#distros directories that are kept, and a list of distros that
#are discarded.
def get_keep_discard_list(distroList, serviceDirectory):
    keep = []
    discard = []

    for i in range(0, len(distroList)):
        distro = distroList[i]
        action = "KEEP"

        #Removal threshold set at 5.
        if(i < 5):
            keep.append(distro)
        else:
            discard.append(distro)
            action = "DISCARD"

        #Log the action taken for the distro, stamping its
        #location, size, action taken, and time of action.
        log(os.path.join(serviceDirectory, distro), get_file_size(os.path.join(serviceDirectory, distro)), action)

    print '\n'
    return keep, discard

#Provided a distro directory, distro size, and action taken
#on distro, output a log to both the console and a .txt file
#outlining the mentioned parameters, along with a time of action.
def log(distro, distroSize, action):

    #Get current time.
    now = datetime.datetime.now()

    #Write to file.
    with open("test.txt", "a") as testFile:
        testFile.write("[" + distro + "]" \
                       "[" + str("%.2f" % distroSize) + "mb]" \
                       "[" + action + "]"\
                       "[" + str(now.month) + '/' + str(now.day) + '/' + str(now.year) + "" \
                       " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]\n")

    #Output to console.
    print "\t[" + distro + "]" \
           "[" + str("%.2f" % distroSize) + "mb]" \
           "[" + action + "]"\
           "[" + str(now.month) + '/' + str(now.day) + '/' + str(now.year) + "" \
           " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]"

#Provided the directory of a file, return its size in MB.
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