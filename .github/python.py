#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import re
#import requests
import os
import json

from pathlib import Path


# Permalinks for File Paths

## Permalink Settings

#permalinks_file= ".github/static-gen/settings/permalinks.md"
#permalinks_file_contents = None

## NEEDS IMPROVEMENT

#PermaLinks = {}
#with open(permalinks_file) as f:
 #       for line in f:
  #              if ":" in line:
   #                     PermaLink, value = line.split('=================END OF PERMALINK SETTINGS============')[0].split(':')  # Needs replaced with regex match 
    #                    PermaLinks[PermaLink] = str(value).rstrip() # needs a value added					
			
#globals().update(PermaLinks)
#output_file = PermaLinks['Blog_PermaLink']





#PUBLIC_GITHUB_MARKDOWN_URL = 'https://api.github.com/markdown'

dirName = ".github/cms/blog_posts"
outputFolder = "blog_posts/"
os.makedirs(outputFolder, exist_ok=True)  # succeeds even if directory exists.
## To do - get all files and contents and convert correctly (Need if statements added for paths like index etc)
## Need to remove paths that were changed for perma links automacially?
def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
       #  Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


var = {}

for file in getListOfFiles(dirName):
  with open(file, 'r') as f:
    for line in f:
        if ":" in line:
          name, value = line.split('=================END OF SEO SETTINGS============')[0].split(':')  # Needs replaced with regex match 
          var[name] = str(value).rstrip() # needs a value added    
          globals().update(var)
	        print(var)
          var.clear()		
