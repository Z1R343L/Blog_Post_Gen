#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import re
#import requests
import os
import json
import time
import platform
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.github/cms/layouts/blog'))
blog_post_template = env.get_template('blog-post.html')

# Used to store key_values for later
var = {}

# Open main settings file
settings_file = ".github/settings.md" 
with open(settings_file, 'r') as f:
  for line in f:
   print(line)
   if ":" in line:
    name, value = line.split('=================END OF SETTINGS============')[0].split(':')  # Needs replaced with regex match 
    var[name] = str(value).rstrip() # needs a value added    
  globals().update(var)
 # print(var)
#print(var)

if var['Asset_Path']:
  AssetPath = var['Asset_Path']
else:
  AssetPath = ""
# Blog Posts for Blog Page

blog_posts = ""

footer_file = ".github/footer.md"
with open(footer_file) as f:
  footer_contents = f.read()

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
      Open_New_Window = 'target="_blank"'
    else:
      Open_New_Window = ""
    if link == "null":
      link = ""
    else:
      link = link
    menu += f"""{position}<a href="{AssetPath}{link}" {Open_New_Window}>{title}</a>"""  
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
outputFolder = "pages/blog/"
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



## https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
          Post_Time = time.strftime('%Y-%m-%d', time.localtime(stat.st_birthtime))
          return Post_Time
        except AttributeError:
          Post_Time = time.strftime('%Y-%m-%d', time.localtime(stat.st_mtime))
          return Post_Time

json_data = ""

content = {}
for file in getListOfFiles(dirName):
  with open(file, 'r') as f:
    

    for line in f:
        if ":" in line:
          name, value = line.split('=================END OF SEO SETTINGS============')[0].split(':')  # Needs replaced with regex match 
          var[name] = str(value).rstrip() # needs a value added    
    globals().update(var)
    try:
      blog_content = f.read().split("=================END OF SEO SETTINGS============",1)[1]    
    except:
      blog_content = f.read()
    content['Blog_Content_Key'] = str(blog_content)
    globals().update(content)
   # file_contents = f.read()
    Facebook_Meta = ""
    BlogTitle = "Blog Post"
    # Write create date for blog post as default	
    BlogDate = ""
    BlogDescription = ""
    SiteTitle = "Site Name"
   # AssetPath = ""
    Facebook_Meta += """<meta property="og:title" content="Blog Post">"""
    data = var 

    try:
      Blog_Contents = content["Blog_Content_Key"]
    except:
      Blog_Contents = ""

    try:
      SiteTitle = data["BlogDate"]
    except:
      SiteTitle = ""

    try:
      BlogTitle = data["Title"]
    except:
      BlogTitle = ""

    try:
      BlogAuthor = data["BlogAuthor"]
    except:
      BlogAuthor = ""

    file_name = outputFolder + Path(file).stem + ".html"
    # For writing blog posts to other page
    blog_posts += f"""  <p class="notice"><strong><a href="{AssetPath}{file_name}">{BlogTitle}</a></strong> <br><br>
{BlogDescription} <p><b>Posted on:</b>{BlogDate}</p></p>
"""	
    ##


    json_data += """
    {
url: """ + f'"{AssetPath}{file_name}",\n' + "name: " +f'"{BlogTitle}",\n' + "contents: " + f'"{BlogDescription}"\n' + "},"
	
    #try:
     #   file_contents = file_contents.split("=================END OF SEO SETTINGS============",1)[1]
   # except:
    #    pass    
    try:
        with open(file_name, 'w') as fh:
          output_from_parsed_template = blog_post_template.render(SiteTitle=SiteTitle,Facebook_Meta=Facebook_Meta,AssetPath=AssetPath,menu=menu,BlogTitle=BlogTitle,BlogAuthor=BlogAuthor,BlogDate=BlogDate,Blog_Contents=Blog_Contents,footer_contents=footer_contents)	
          fh.write(output_from_parsed_template)
	    
    except IOError:
        sys.exit(u'Unable to write to files: {0}'.format(file_contents))  
    var.clear()
    content.clear()


index_file_name = "pages/blog/index.html"
try:
    with codecs.open(index_file_name, 'w', encoding='utf-8') as f:
        f.write(f"""<head>
    <meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>News | Simply Docs</title>
<meta name="description" content="A showcase of Simply Docs by MarketingPipeline built using Simple.CSS">

 
<link rel="stylesheet" href="{AssetPath}assets/style.css">

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
  
 
{menu}
</nav>

        <h1>Blog</h1>
      <p>Latest Blog Posts</p>
    </header>


<main>
{blog_posts}



</main>

<footer>
     {footer_contents}
    </footer>

   
 <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag.js"></script> 
""")
except IOError:
    sys.exit('Index file does not exist, or has no content.  Exiting')  








## Create search file


search_file_name = "pages/blog/search.html"
try:
    with codecs.open(search_file_name, 'w', encoding='utf-8') as f:
        f.write(""" 

<script>
if (window.location.href.indexOf("/pages/blog/search?") != -1) {

window.onload=function(){
     var url_string = window.location.href
      var url = new URL(url_string);
var c = url.searchParams.get("posts");
console.log(c);
     
      
     
     if (c === null){
document.body.innerHTML = "No search route provided"
       
     } else {
       """ + f"""
         const input = [
{json_data}""" + """
{
url: "www.google.com3",
name: "name1"
}
]


let url = c

var blogPosts = ""

var SearchResults = false
input.forEach(object => {
  if(object.url.includes(url)) {
  blogPosts += object.url
  SearchResults = true  
  } 
})
       
       if (url == ""){
        SearchResults = false 
         var Message = "No search query was provided"
       } else {
         var Message = "No blog posts found for " + c
       }
       
       
          
     if (url === null){
 SearchResults = false 
 var Message = "No search route provided"
       
     } 
       if (SearchResults === true) {
         
         document.body.innerHTML = ` Blog posts found containing:  ${c}  
         <br>
  
         ${blogPosts} `
         
       } else {
          document.body.innerHTML = Message
       }
         
       
       
     }
     
    }
} else {
  // Do nothing
}
    
</script>
        
""")
except IOError:
    sys.exit('Blog posts do not exist, or has no content.  Exiting')  