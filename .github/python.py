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

permalinks_file= ".github/static-gen/settings/permalinks.md"
permalinks_file_contents = None

## NEEDS IMPROVEMENT

PermaLinks = {}
with open(permalinks_file) as f:
        for line in f:
                if ":" in line:
                        PermaLink, value = line.split('=================END OF PERMALINK SETTINGS============')[0].split(':')  # Needs replaced with regex match 
                        PermaLinks[PermaLink] = str(value).rstrip() # needs a value added					
			
globals().update(PermaLinks)
output_file = PermaLinks['Blog_PermaLink']





#PUBLIC_GITHUB_MARKDOWN_URL = 'https://api.github.com/markdown'

dirName = ".github/static-gen/content"

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



for file in getListOfFiles(dirName):
    with open(file, 'r') as f:
        file_contents = f.read()
        file_contents = file_contents
        # Grab only the file name from the string


        # Need to work on putting files in right locations with permalink functions 
        if ".github/static-gen/content/" in file:
          try:
             file_contents = file_contents.split("=================END OF SEO SETTINGS============",1)[1] # Get all after before SEO settings
          except:
            ## If file does not contain settings (pass) for now. Will be future requirement 
            pass


       ## This does NOT work 
        
      #  if ".github/static-gen/content/blog_posts/" in file: 
     #     ## If blog post - define template & grab file path and more here.
    #      Template = f"""<link rel="stylesheet" href="./assets/style.css">
   #       <h1> Example Blop Post</h1>
	#<body>{file_contents}</body>
	 #  <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag-GitHub.js"></script> 
	#"""

        if "index" in file: 
          Template = f"""<link rel="stylesheet" href="./assets/style.css">
	<body>{file_contents}</body>
	   <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag-GitHub.js"></script> 
	"""
          FilePath = ""
        else:
          Template = f"""<link rel="stylesheet" href="./assets/style.css">
	<body>{file_contents}</body>
	   <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag-GitHub.js"></script> 
	"""
          FilePath = "test/"   

        file_name = FilePath + Path(file).stem + ".html"

        try:
          with codecs.open(file_name, 'w', encoding='utf-8') as f:
            f.write(Template)
        except IOError: 
         sys.exit(u'Unable to write to files: {0}'.format(file_contents))  
  

    



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
#output_file = PermaLinks['Blog_PermaLink'] + "blog_post.html"
# Define Input File Names / Paths Here


#os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Blog File Example
input_file = ".github/static-gen/content/blog_posts/EXAMPLE.MD"
input_file_contents = None

# Index File
#index_file = ".github/static-gen/content/index.md"
#index_file_contents = None

# Setting(s) Files

## Nav Menu
#nav_menu_settings_file= "./content/settings/nav_menu.md"
#nav_menu_settings_file_contents = None




# Define Output File Names Here
#index_output_file = "index.html"


# Open the templates
#blog_post_template = ".github/static-gen/html_templates/blog_post.html"

#try:
 #   with open(blog_post_template, 'r') as f:
  #      blog_post_template_contents = f.read()
#except IOError:
 #   sys.exit('Template does not exist, or has no content.  Exiting')



# Open our file and
#try:
   # with open(input_file, 'r') as f:
  #      input_file_contents = f.read()
 #       input_file_contents = input_file_contents.split("=================END OF SEO SETTINGS============",1)[1] # Get all after before SEO settings
        
#except IOError:
 #   sys.exit('Input file does not exist, or has no content.  Exiting')

# Open Index File

#try:
  #  with open(index_file, 'r') as f:
 #       index_file_contents = f.read()
        
        
#except IOError:
 #   sys.exit('Input file does not exist, or has no content.  Exiting')





#var = {}
#with open(input_file) as conf:
 #       for line in conf:
 #               if ":" in line:
  #                      name, value = line.split('=================END OF SEO SETTINGS============')[0].split(':')  # Needs replaced with regex match 
   #                     var[name] = str(value).rstrip() # needs a value added

#globals().update(var)	

#NavMenuLinks = {}
#with open(nav_menu_settings_file) as nav_menu_file:
 #       for line in nav_menu_file:
  #              if ":" in line:
   #                     Link, value = line.split('=================END OF NAV MENU============')[0].split(':')  # Needs replaced with regex match 
    #                    NavMenuLinks[Link] = str(value).rstrip() # needs a value added		
			
			

    
# Set github url
#github_url = PUBLIC_GITHUB_MARKDOWN_URL

# Make the request to github to create markdown
#payload = {"text": input_file_contents, "mode": "markdown"}
#html_response = requests.post(github_url, json=payload)

# Determine our output file
#if output_file:
 #   output_file = output_file
#else:
 #   output_file = u'{0}.html'.format(input_file)

# ensure we have a .html suffix on our file
#if index_output_file[-5:] != '.html':
#    index_output_file += '.html'

#if index_output_file:
 #   index_output_file = index_output_file
#else:
 #   index_output_file = u'{0}.html'.format(index_file)

# ensure we have a .html suffix on our file
#if index_output_file[-5:] != '.html':
 #   index_output_file += '.html'



#NavMenu = NavMenuLinks

#if not NavMenu['Link']:
 # NavMenu_Content = ""
#else:
 # NavMenu_Content = NavMenu['Link']


#for value in NavMenu:
#	print(value)




# Open our file and
try:
    with open(input_file, 'r') as f:
        input_file_contents = f.read()
        input_file_contents = input_file_contents.split("=================END OF SEO SETTINGS============",1)[1] # Get all after before SEO settings
        
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')

# Open Index File

#try:
  #  with open(index_file, 'r') as f:
 #       index_file_contents = f.read()
        
        
#except IOError:
   # sys.exit('Input file does not exist, or has no content.  Exiting')





var = {}
with open(input_file) as conf:
        for line in conf:
                if ":" in line:
                        name, value = line.split('=================END OF SEO SETTINGS============')[0].split(':')  # Needs replaced with regex match 
                        var[name] = str(value).rstrip() # needs a value added

globals().update(var)	

#NavMenuLinks = {}
#with open(nav_menu_settings_file) as nav_menu_file:
 #       for line in nav_menu_file:
  #              if ":" in line:
   #                     Link, value = line.split('=================END OF NAV MENU============')[0].split(':')  # Needs replaced with regex match 
    #                    NavMenuLinks[Link] = str(value).rstrip() # needs a value added		
			
			

    
# Set github url
#github_url = PUBLIC_GITHUB_MARKDOWN_URL

# Make the request to github to create markdown
#payload = {"text": input_file_contents, "mode": "markdown"}
#html_response = requests.post(github_url, json=payload)

# Determine our output file
#if output_file:
 #   output_file = output_file
#else:
 #   output_file = u'{0}.html'.format(input_file)

# ensure we have a .html suffix on our file
#if index_output_file[-5:] != '.html':
#    index_output_file += '.html'

#if index_output_file:
 #   index_output_file = index_output_file
#else:
 #   index_output_file = u'{0}.html'.format(index_file)

# ensure we have a .html suffix on our file
#if index_output_file[-5:] != '.html':
 #   index_output_file += '.html'



#NavMenu = NavMenuLinks

#if not NavMenu['Link']:
 # NavMenu_Content = ""
#else:
 # NavMenu_Content = NavMenu['Link']


#for value in NavMenu:
#	print(value)

data = var 

BlogTitle = data['BlogTitle']
if not data['BlogDate']:
  BlogDate = ""
else:
  BlogDate = data['BlogDate']

if not data['SEO_Title']:
  SiteTitle = "Site Name"
else:
  SiteTitle = data['SEO_Title'] + "| Site Name"

Facebook_Meta = ""

if not data['OG_Title']:
  pass
else:
  Facebook_Meta += """<meta property="og:title" content="Simply Docs Demo">"""

if not data['OG_Image']:
  pass
else:
  Facebook_Meta += """<meta property="og:image" content="./assets/images/OG_image.png">"""


if not data['OG_URL']:
  pass
else:
  Facebook_Meta += """<meta property="og:url" content="https://marketingpipeline.github.io/Simply-Docs/">"""

if not data['OG_Type']:
  pass
else:
  Facebook_Meta += """<meta property="og:type" content="article">"""

if not data['OG_Description']:
  pass
else:
  Facebook_Meta += """<meta property="og:description" content="A Simply Docs / Blog Template built using Simple.css.">"""


output_file = output_file + "blog_post_SEO_test.html"

# Write the file out that we have created
try:
    with codecs.open(output_file, 'w', encoding='utf-8') as f:
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
   input_file_contents + """
    </div>
	</body>
	 <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag-GitHub.js"></script> 
	""")
except IOError:
    sys.exit(u'Unable to write to file: {0}'.format(output_file))




# Write the index file out
#try:
 #   with codecs.open(index_output_file, 'w', encoding='utf-8') as f:
  #      f.write(f"""
	#<link rel="stylesheet" href="./assets/style.css">
	#<body>{index_file_contents}</body>
	#   <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag-GitHub.js"></script> 
	#""")
#except IOError: 
 #   sys.exit(u'Unable to write to file: {0}'.format(index_output_file))
