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


## Create Blog Posts
content = {}
for file in getListOfFiles(dirName):
  with open(file, 'r') as f:
    

    for line in f:
        if ":" in line:
	  # Create JSON Data	
          name, value = line.split('=================END OF SEO SETTINGS============')[0].split(':')  # Needs replaced with regex match 
          var[name] = str(value).rstrip() # needs a value added    
    globals().update(var)
    
	
    ## Get input after 	(ERROR HERE)
    try:
      blog_content = f.read().split("=================END OF SEO SETTINGS============",1)[1]    
    except:
    # If no settings - get the whole file contents		
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
      SiteTitle = data["SEO_Title"]
    except:
      SiteTitle = ""


    try:
      BlogDate = data["BlogDate"]
    except:
      BlogDate= creation_date(file)


    try:
      BlogTitle = data["BlogTitle"]
    except:
      BlogTitle = ""

    try:
      BlogAuthor = data["BlogAuthor"]
      BlogAuthor_LowerCase = BlogAuthor.lower
    except:
      BlogAuthor = ""

    try:
      BlogDescription = data["BlogDescription"]
    except:
      BlogDescription = ""

    file_name = outputFolder + Path(file).stem + ".html"
    # For writing blog posts to other page
    blog_posts += f"""  <p class="notice"><strong><a href="{AssetPath}{file_name}">{BlogTitle}</a></strong> <br><br>
{BlogDescription} <p><b>Posted on:</b>{BlogDate}</p></p>
"""	
    ##


    json_data += """
    {
url: """ + f'"{AssetPath}{file_name}",\n' + "name: " +f'"{BlogTitle}",\n' + "contents: " + f'"{BlogDescription},"\n' + "published: " + f'"{BlogDate},"\n' + "},"
	
    #try:
     #   file_contents = file_contents.split("=================END OF SEO SETTINGS============",1)[1]
   # except:
    #    pass    
    try:
        with open(file_name, 'w') as fh:
          output_from_parsed_template = blog_post_template.render(menu=menu,SiteTitle=SiteTitle,Facebook_Meta=Facebook_Meta,AssetPath=AssetPath,BlogTitle=BlogTitle,BlogAuthor=BlogAuthor, BlogAuthor_LowerCase = BlogAuthor_LowerCase,BlogDate=BlogDate,Blog_Contents=Blog_Contents,footer_contents=footer_contents)	
          fh.write(output_from_parsed_template)
	    
    except IOError:
        sys.exit(u'Unable to write to files: {0}'.format(file_contents))  
    var.clear()
    content.clear()

	
# Create page showing all blog posts (blog index file)	
blog_index_template = env.get_template('blog-index.html')
index_file_name = "pages/blog/index.html"
output_from_parsed_template = blog_index_template.render(AssetPath=AssetPath,menu=menu,blog_posts=blog_posts,footer_contents=footer_contents)	
try:
    with open(index_file_name, 'w') as fh:
        fh.write(output_from_parsed_template)
except IOError:
    sys.exit('Index file does not exist, or has no content.  Exiting')  





# Create Blog Author Pages
blog_author_template = env.get_template('blog-author.html')
content = {}
dirName = ".github/cms/blog_posts/author"
outputFolder = "pages/blog/author/"
os.makedirs(outputFolder, exist_ok=True)
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
      SiteTitle = data["SEO_Title"]
    except:
      SiteTitle = ""


    try:
      BlogAuthor = data["BlogAuthor"]
    except:
      BlogAuthor = ""

    file_name = outputFolder + Path(file).stem + ".html"
    # For writing blog posts to other page
    #try:
     #   file_contents = file_contents.split("=================END OF SEO SETTINGS============",1)[1]
   # except:
    #    pass    
    try:
        with open(file_name, 'w') as fh:
          output_from_parsed_template = blog_author_template.render(menu=menu,SiteTitle=SiteTitle,Facebook_Meta=Facebook_Meta,AssetPath=AssetPath,footer_contents=footer_contents)	
          fh.write(output_from_parsed_template)
	    
    except IOError:
        sys.exit(u'Unable to write to files: {0}'.format(file_contents))  
    var.clear()
    content.clear()



	
	
	
	

# SWtiching template path
env = Environment(loader=FileSystemLoader('.github/cms/layouts'))

# Create search page
search_page_template = env.get_template('search.html')
search_file_name = "pages/seach.html"
output_from_parsed_template = search_page_template.render(AssetPath=AssetPath,menu=menu,footer_contents=footer_contents)	
try:
    with open(search_file_name, 'w') as fh:
        fh.write(output_from_parsed_template)
except IOError:
    sys.exit('Seach page file does not exist, or has no content.  Exiting')  




## Create search JS file
search_file_name = "assets/js/blog-search.js"
try:
    with codecs.open(search_file_name, 'w', encoding='utf-8') as f:
        f.write(""" 

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
    

        
""")
except IOError:
    sys.exit('Blog posts do not exist, or has no content.  Exiting')  
