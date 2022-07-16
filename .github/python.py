#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import re
#import requests
import os
import json

from pathlib import Path


# Blog Posts for Blog Page

blog_posts = ""

# Permalinks for File Paths

## Permalink Settings

permalinks_file= "navlinks.md"
permalinks_file_contents = None

## NEEDS IMPROVEMENT

#PermaLinks = {}
menu=""
pattern = 'Link:(.*?) New_Window:(.*?) Title:(.*?) Position:(.*?)'
with open(permalinks_file) as f:
  file_contents = f.read()
  for (link, window, title, position) in re.findall(pattern, file_contents, re.DOTALL):
    if window == "True":
      Open_New_Window = "__target blank"
    else:
      Open_New_Window = "__target blank"
    menu += f"""{position}<a href="{link}" {Open_New_Window}>{title}</a>"""  
   #print(link, window, title, position)
 # for (link, window, title, position) in re.findall(pattern, file_contents, re.DOTALL):
  #  for value in link:
   #  print(link, window, title, position)
    #  print(link, window, title, position)	
	#file_contents = f.read()       
        #for line in file_contents:
                #for (link, window, title, position) in re.findall(pattern, s):
                 # print(link, window, title, position)		
#globals().update(PermaLinks)
#print(PermaLinks)
#output_file = PermaLinks['Test']


#PUBLIC_GITHUB_MARKDOWN_URL = 'https://api.github.com/markdown'

dirName = ".github/cms/blog_posts"
outputFolder = "blog_posts/"
os.makedirs(outputFolder, exist_ok=True)

outputFolder2 = "pages/"
os.makedirs(outputFolder2, exist_ok=True)

# succeeds even if directory exists.
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
    file_contents = f.read()       


    Facebook_Meta = ""
    BlogTitle = "Blog Post"
    BlogDate = ""
    BlogDescription = ""
    SiteTitle = "Site Name"
    Facebook_Meta += """<meta property="og:title" content="Blog Post">"""
    try:
        data = var 
        BlogTitle = data["SEO_Title"]
        BlogDate =  data["BlogDate"]
        SiteTitle = data["BlogDate"]
    except KeyError:
        pass
    file_name = outputFolder + Path(file).stem + ".html"
    # For writing blog posts to other page
    blog_posts += f"""  <p class="notice"><strong><a href=".{file_name}">{BlogTitle}</a></strong> <br><br>
{BlogDescription} <p><b>Posted on:</b>{BlogDate}</p></p>
"""	
	
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


<link rel="stylesheet" href="./assets/style.css">
     </head>""" + 
     f"""<header>
<nav>
  
 {menu}
</nav>

		    <h1>{BlogTitle} t</h1>
		    <p>Published: {BlogDate} <br>by <a href="/Simply-Docs/pages/author">Author</a></p>
		    </header>
    <main>
<article>
		    {file_contents}
 </article>
    </main>

	 <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag-GitHub.js"></script> 
<footer>
      <p> Hello</p>
  <small>© 2014 Some company name</small>
      <address>email@email.com</address>
    </footer>		 
	""")
    except IOError:
        sys.exit(u'Unable to write to files: {0}'.format(file_contents))  
    var.clear()


index_file_name = "pages/blog_posts.html"
try:
    with codecs.open(index_file_name, 'w', encoding='utf-8') as f:
        f.write(f"""<head>
    <meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>News | Simply Docs</title>
<meta name="description" content="A showcase of Simply Docs by MarketingPipeline built using Simple.CSS">

 
<link rel="stylesheet" href="./assets/style.css">

<link rel="icon" href="/Simply-Docs/assets/images/favicon.png">
<link rel="apple-touch-icon" href="/Simply-Docs/assets/images/favicon.png">

 <!-- Facebook integration -->
<meta property="og:title" content="Simply Docs Demo">
<meta property="og:image" content="/Simply-Docs/assets/images/OG_image.png">
<meta property="og:url" content="https://marketingpipeline.github.io/Simply-Docs/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Simple.css">
<meta property="og:description" content="A Simply Docs / Blog Template built using Simple.css.">

<!-- Twitter integration -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Simply Docs | Demo">
<meta name="twitter:image" content="/Simply-Docs/assets/images/OG_image.png">
<meta name="twitter:url" content="https://marketingpipeline.github.io/Simply-Docs/">
<meta name="twitter:description" content="A Simply Docs / Blog Template built using Simple.css">

<script src="https://cdn.jsdelivr.net/npm/prismjs@1.28.0/prism.min.js"></script>
  </head>
<header>
     <nav>
  
  <a href="/Simply-Docs/">Home</a>
  
  <a href="/Simply-Docs/pages/documentation">Docs</a>
  
  <a href="https://github.com/MarketingPipeline/Simply-Docs/archive/refs/heads/main.zip">Download</a>
  
  <a href="/Simply-Docs/pages/news">News</a>
  
  <a href="https://github.com/MarketingPipeline/Simply-Docs"><svg class="icon" viewBox="0 0 32 32"><path d="M16 0.395c-8.836 0-16 7.163-16 16 0 7.069 4.585 13.067 10.942 15.182 0.8 0.148 1.094-0.347 1.094-0.77 0-0.381-0.015-1.642-0.022-2.979-4.452 0.968-5.391-1.888-5.391-1.888-0.728-1.849-1.776-2.341-1.776-2.341-1.452-0.993 0.11-0.973 0.11-0.973 1.606 0.113 2.452 1.649 2.452 1.649 1.427 2.446 3.743 1.739 4.656 1.33 0.143-1.034 0.558-1.74 1.016-2.14-3.554-0.404-7.29-1.777-7.29-7.907 0-1.747 0.625-3.174 1.649-4.295-0.166-0.403-0.714-2.030 0.155-4.234 0 0 1.344-0.43 4.401 1.64 1.276-0.355 2.645-0.532 4.005-0.539 1.359 0.006 2.729 0.184 4.008 0.539 3.054-2.070 4.395-1.64 4.395-1.64 0.871 2.204 0.323 3.831 0.157 4.234 1.026 1.12 1.647 2.548 1.647 4.295 0 6.145-3.743 7.498-7.306 7.895 0.574 0.497 1.085 1.47 1.085 2.963 0 2.141-0.019 3.864-0.019 4.391 0 0.426 0.288 0.925 1.099 0.768 6.354-2.118 10.933-8.113 10.933-15.18 0-8.837-7.164-16-16-16z"></path></svg>Github</a>
  
</nav>

        <h1>News</h1>
      <p>Newest updates about this project</p>
    </header>


<main>
{blog_posts}



</main>

<footer>
      <p>Simply Docs was created by <a href="https://github.com/MarketingPipeline/">Marketing Pipeline</a> and is licensed under the MIT license.</p>
  <small>© 2014 Some company name</small>
      <address>email@email.com</address>
    </footer>

   
 <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag.js"></script> 
""")
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')  
