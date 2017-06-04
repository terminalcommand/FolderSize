import os
import logging
from os.path import join, getsize
import re

def bytes2human(size):
    gibi = 1024*1024*1024
    mibi = 1024*1024
    kibi = 1024
    if size >= gibi:
        return str(round(size/gibi, 2))+" GiB"
    elif size >= mibi:
        return str(round(size/mibi, 2))+" MiB"
    elif size >= kibi:
        return str(round(size/kibi, 2))+" KiB"
    else:
        return str(size)+" Bytes"

def clearsize(foldername):
    match = re.search("\(\d+(\.\d+)?.(Bytes|GiB|MiB|KiB)\)",
                      foldername)
    if match:
        stripped = \
        foldername[:match.start()] + foldername[match.end():]
#        print("Stripped: "+stripped)
        return stripped
    else:
        return foldername


def renamedir(startpath=os.curdir):
    rootname = os.getcwd()
    size = 0

    for root, dirs, files in os.walk(startpath, topdown=True):
        for name in files:
            filepath = join(root, name)
            size += getsize(filepath)
            
    try:
        desc = '('+bytes2human(size)+')'
        cleared = clearsize(rootname)
        #        print("Rootname: "+ rootname)
        #        print("Cleared: "+cleared)
        os.replace(rootname, cleared+desc)

        print("Successfully renamed dir to", cleared+desc)
       
    except Exception as err:
        logging.error(err)

for root, dirs, files in os.walk(os.curdir, topdown=True):
    rootname = os.getcwd()
    renamedir()
    rootname = os.getcwd()
    for folder in dirs:
        folderpath=join(rootname,folder)
        os.chdir(folderpath)

        renamedir()
