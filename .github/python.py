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

varCounter = 0 
for file in getListOfFiles(dirName):
  with open(file, 'r') as f:
    file_contents = f.read()
    for line in f:
        if ":" in line:
          name, value = line.split('=================END OF SEO SETTINGS============')[0].split(':')  # Needs replaced with regex match 
          var[name] = str(value).rstrip() # needs a value added    
  globals().update(var)
  ## 
  			
  data = var 
  Facebook_Meta = ""
  BlogTitle = "Blog Post"
  BlogDate = ""
  SiteTitle = "Site Name"

  Facebook_Meta += """<meta property="og:title" content="Blog Post">"""
  try:

      BlogTitle = data["SEO_Title"]
      BlogDate =  data["BlogDate"]
      SiteTitle = data["BlogDate"]
  except KeyError:
        pass

      
	

  file_name = outputFolder + Path(file).stem + ".html"
  try:
      file_contents = file_contents.split("=================END OF SEO SETTINGS============",1)[1]
  except:
      pass
  try:
    with codecs.open(file_name, 'w', encoding='utf-8') as f:
      f.write(f"""<head><title>{SiteTitle}</title>
            <meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.28.0/prism.min.js"></script>
{Facebook_Meta}         
     </head>""" + """
	<style>
	
	/**
 * GHColors theme by Avi Aryan (http://aviaryan.in)
 * Inspired by Github syntax coloring
 */
code[class*="language-"],
pre[class*="language-"] {
	color: #393A34;
	font-family: "Consolas", "Bitstream Vera Sans Mono", "Courier New", Courier, monospace;
	direction: ltr;
	text-align: left;
	white-space: pre;
	word-spacing: normal;
	word-break: normal;
	font-size: .9em;
	line-height: 1.2em;
	-moz-tab-size: 4;
	-o-tab-size: 4;
	tab-size: 4;
	-webkit-hyphens: none;
	-moz-hyphens: none;
	-ms-hyphens: none;
	hyphens: none;
}
pre > code[class*="language-"] {
	font-size: 1em;
}
pre[class*="language-"]::-moz-selection, pre[class*="language-"] ::-moz-selection,
code[class*="language-"]::-moz-selection, code[class*="language-"] ::-moz-selection {
	background: #b3d4fc;
}
pre[class*="language-"]::selection, pre[class*="language-"] ::selection,
code[class*="language-"]::selection, code[class*="language-"] ::selection {
	background: #b3d4fc;
}
/* Code blocks */
pre[class*="language-"] {
	padding: 1em;
	margin: .5em 0;
	overflow: auto;
	border: 1px solid #dddddd;
	background-color: white;
}
/* Inline code */
:not(pre) > code[class*="language-"] {
	padding: .2em;
	padding-top: 1px;
	padding-bottom: 1px;
	background: #f8f8f8;
	border: 1px solid #dddddd;
}
.token.comment,
.token.prolog,
.token.doctype,
.token.cdata {
	color: #999988;
	font-style: italic;
}
.token.namespace {
	opacity: .7;
}
.token.string,
.token.attr-value {
	color: #e3116c;
}
.token.punctuation,
.token.operator {
	color: #393A34; /* no highlight */
}
.token.entity,
.token.url,
.token.symbol,
.token.number,
.token.boolean,
.token.variable,
.token.constant,
.token.property,
.token.regex,
.token.inserted {
	color: #36acaa;
}
.token.atrule,
.token.keyword,
.token.attr-name,
.language-autohotkey .token.selector {
	color: #00a4db;
}
.token.function,
.token.deleted,
.language-autohotkey .token.tag {
	color: #9a050f;
}
.token.tag,
.token.selector,
.language-autohotkey .token.keyword {
	color: #00009f;
}
.token.important,
.token.function,
.token.bold {
	font-weight: bold;
}
.token.italic {
	font-style: italic;
}
	
	
	body { 
    margin: 0;   /* Remove body margins */
}
	.banner {
  background-image: linear-gradient(rgba(39, 71, 118, 0.6), rgba(39, 71, 118, 0.6)), url(https://images.unsplash.com/photo-1509136561942-7d8663edaaa2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1055&q=80);
  background-size: cover;
  background-position: center;
  color: white;
  text-shadow: 0 0 10px rgba(0,0,0,0.2);
  padding: 80px 0px;
}
.banner h1 {
  font-size: 40px;
  margin-top: 0;
  opacity: 0.8;
}
.banner p {
  font-size: 25px;
  margin-bottom: 0;
  opacity: 0.9;
  font-weight: lighter;
}
.container {
  width: 900px;
  margin: 0px auto;
}
.blogpost-content h2 {
  margin-top: 50px;
  opacity: 0.4;
  font-weight: bolder;
}
.blogpost-content p {
  font-weigh: lighter;
  
}
@media(max-width: 992px) {
  .container {
    width: 700px;
  }
}
@media(max-width: 768px) {
  .container {
    width: 500px;
  }
}
@media(max-width: 480px) {
  .container {
    width: 350px;
  }
}
</style>
<!-- Image and text -->
<body>
<div class="banner">
      <div class="container">""" +
     f"<h1>{BlogTitle} t</h1>" + 
        f"<p>{BlogDate}</p>" + """
      </div>
    </div>
    <div class="container blogpost-content"> """ +
   file_contents + """
    </div>
	</body>
	 <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag-GitHub.js"></script> 
	""")
    data.clear()

  except IOError: 
        sys.exit(u'Unable to write to files: {0}'.format(file_contents)) 
         

                 
       