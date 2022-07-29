#! /usr/bin/env python
# -*- coding: utf-8 -*-

########################################
#              Import(s)               #
########################################    

import codecs
import sys
import re
import os
import json
import time
import platform
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


########################################
#          End of Import(s)            #
########################################    








########################################
#              List(s)                 #
########################################    


# Variables to append / add for usage later in this script

## Used to store JSON key_values for later
var = {}

## Blog Posts for Blog Page
blog_posts = ""

## JSON data
json_data = ""



########################################
#          End of Lists(s)             #
########################################    









########################################
#            Function(s)               #
########################################    

## function to get all files in directory
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



## Function to get File Creation Dates
# https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
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



########################################
#          End of Function(s)          #
########################################    










########################################
#           SITE SETTINGS              #
########################################    

## Open main settings file
settings_file = ".github/settings.md" 
with open(settings_file, 'r') as f:
  for line in f:
   ## Make JSON Key Values
   if ":" in line:
    name, value = line.split('=================END OF SETTINGS============')[0].split(':')  
    var[name] = str(value).rstrip()   
  globals().update(var)


if var['Asset_Path']:
  AssetPath = var['Asset_Path']
else:
  AssetPath = ""



if var['Site_Name']:
  Site_Name = var['Site_Name']
else:
  Site_Name = ""



## Get the footer contents
footer_file = ".github/footer.md"
with open(footer_file) as f:
  footer_contents = f.read()



## Create menu links


permalinks_file= "navlinks.md"
permalinks_file_contents = None
menu=""
## Regex match for menu links

pattern = 'Link:(.*?) New_Window:(.*?) Title:(.*?) External_URL:(.*?),'
# old match
#pattern = 'Link:(.*?) New_Window:(.*?) Title:(.*?) Position:(.*?) External_URL:(.*?)'
with open(permalinks_file) as f:
  file_contents = f.read()
  for (link, window, title, external_link) in re.findall(pattern, file_contents, re.DOTALL):
    ## For opening link in a new window		
    if window == "True":
      Open_New_Window = 'target="_blank"'
    else:
      Open_New_Window = ""
    ## For home pages (example : "/")
    if link == "null":
      link = ""
    else:
      link = link
    print(external_link)
    if external_link == "True":
	    print("true")
	    path = ""
    else:
	    path = AssetPath 
    menu += f"""<a href="{path}{link}" {Open_New_Window}>{title}</a>"""  		
   ## For links like github.com/MarketingPipeline (does not add asset path infront) if not False
    


########################################
#      END OF SITE SETTINGS            #
########################################    






########################################
#           SITE SETTINGS              #
########################################    




########################################
#             Index File               #
########################################    

env = Environment(loader=FileSystemLoader('.github/cms/layouts'))
template = env.get_template('index.html')

# Open Index File Content
index_file_contents = ".github/index.md"
try:
    with open(index_file_contents, 'r') as f:
        index_file_contents = f.read()
        
        
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')

index_file_name = "index.html"
output_from_parsed_template = template.render(menu=menu, Site_Name=Site_Name,index_file_contents=index_file_contents,footer_contents=footer_contents)

try:
    with open(index_file_name, 'w') as fh:
        fh.write(output_from_parsed_template)
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')  

########################################
#          End Of Index File           #
########################################    






########################################
#               BLOG                   #
########################################      

## Make folder for blog posts
outputFolder = "pages/blog/"

dirName = ".github/cms/blog_posts"

## succeeds even if directory does not exist.
os.makedirs(outputFolder, exist_ok=True)

## Create Blog Posts With All Files Returned

env = Environment(loader=FileSystemLoader('.github/cms/layouts/blog'))
blog_post_template = env.get_template('blog-post.html')
content = {}
for file in getListOfFiles(dirName):
  with open(file, 'r') as f:
    if "/author/" in file:
      break
    for line in f:
        #if "=================END OF SEO SETTINGS============" in line:
         # print("Found")
        #else:
         # print("Not Found")  
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
   
    data = var 

    try:
      Blog_Contents = content["Blog_Content_Key"]
    except:
      Blog_Contents = ""

    try:
      SiteTitle = data["SEO_Title"]
    except:
      SiteTitle = "Blog Post"


    try:
      BlogDate = data["BlogDate"]
    except:
      BlogDate= creation_date(file)


    try:
      BlogTitle = data["BlogTitle"]
    except:
      BlogTitle = "Blog Post"

    try:
      BlogAuthor = data["BlogAuthor"]
      BlogAuthor_LowerCase = BlogAuthor.lower()
    except:
      BlogAuthor = ""
      BlogAuthor_LowerCase = ""

    try:
      BlogDescription = data["BlogDescription"]
    except:
      BlogDescription = ""

    # Create SEO / Meta Tags
    try:
      Facebook_Meta += f"""<meta property="og:title" content="{data["OG_Title"]}">""" 
    except:
      pass

    file_name = outputFolder + Path(file).stem + ".html"
    # For writing blog posts to other page > (pages/blog/index.html)
    blog_posts += f"""  <p class="notice"><strong><a href="{AssetPath}{file_name}">{BlogTitle}</a></strong> <br><br>
{BlogDescription} <p><b>Posted on:</b>{BlogDate}</p></p>
"""	
    

    # For writing JSON data for github.com/MarketingPipeline/Static-Search.js
    json_data += """
    {
url: """ + f'"{AssetPath}{file_name}",\n' + "name: " +f'"{BlogTitle}",\n' + "contents: " + f'"{BlogDescription}",\n' + "published: " + f'"{BlogDate}",\n' + "},"
	
    #try:
     #   file_contents = file_contents.split("=================END OF SEO SETTINGS============",1)[1]
   # except:
    #    pass    
    try:
        with open(file_name, 'w') as fh:
          output_from_parsed_template = blog_post_template.render(menu=menu,Site_Name=Site_Name,SiteTitle=SiteTitle,Facebook_Meta=Facebook_Meta,AssetPath=AssetPath,BlogTitle=BlogTitle,BlogAuthor=BlogAuthor, BlogAuthor_LowerCase = BlogAuthor_LowerCase,BlogDate=BlogDate,Blog_Contents=Blog_Contents,footer_contents=footer_contents)	
          fh.write(output_from_parsed_template)
	    
    except IOError:
        sys.exit(u'Unable to write to files: {0}'.format(file_contents))
    # Delete the JSON keys made for the file & start loop again till done	
    var.clear()
    content.clear()


	
## Create page showing all blog posts (blog index file)	
blog_index_template = env.get_template('blog-index.html')
index_file_name = "pages/blog/index.html"
output_from_parsed_template = blog_index_template.render(Site_Name=Site_Name, AssetPath=AssetPath,menu=menu,blog_posts=blog_posts,footer_contents=footer_contents)	
try:
    with open(index_file_name, 'w') as fh:
        fh.write(output_from_parsed_template)
except IOError:
    sys.exit('Blog index file template does not exist, or has no content.  Exiting')  


## Create Blog Author Pages
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
    Facebook_Meta += """<meta property="og:title" content="Blog Post">"""
    data = var 

    try:
      SiteTitle = data["SEO_Title"]
    except:
      SiteTitle = "Author Page"


    try:
      PageTitle = data["PageTitle"]
    except:
      PageTitle = "Author"

    file_name = outputFolder + Path(file).stem + ".html"   
    try:
        with open(file_name, 'w') as fh:
          output_from_parsed_template = blog_author_template.render(Site_Name=Site_Name,menu=menu,SiteTitle=SiteTitle,PageTitle=PageTitle,Facebook_Meta=Facebook_Meta,AssetPath=AssetPath,footer_contents=footer_contents)	
          fh.write(output_from_parsed_template)
	    
    except IOError:
        sys.exit(u'Unable to write to files: {0}'.format(file_contents))  
    var.clear()
    content.clear()

########################################
#            End of Blog               #
########################################      








########################################
#            Search Route              #
########################################      

## Create search route page
search_page_template = env.get_template('search-route.html')
search_file_name = "pages/blog/search.html"
output_from_parsed_template = search_page_template.render(Site_Name=Site_Name, AssetPath=AssetPath,menu=menu,footer_contents=footer_contents)	
try:
    with open(search_file_name, 'w') as fh:
        fh.write(output_from_parsed_template)
except IOError:
    sys.exit('Seach route page file does not exist, or has no content.  Exiting')  
	
	
	
	

## Switching template path
env = Environment(loader=FileSystemLoader('.github/cms/layouts'))

## Create search page
search_page_template = env.get_template('search.html')
search_file_name = "pages/search.html"
output_from_parsed_template = search_page_template.render(Site_Name=Site_Name, AssetPath=AssetPath,menu=menu,footer_contents=footer_contents)	
try:
    with open(search_file_name, 'w') as fh:
        fh.write(output_from_parsed_template)
except IOError:
    sys.exit('Seach page template file does not exist, or has no content.  Exiting')  






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

########################################
#         End of Search Route          #
########################################      




########################################
#            Documentation             #
########################################      

documentation_template = env.get_template('documentation.html')

## Open Input Documenation Content

# Need to create a better documenation function than just one page! 
documenation_file_contents = ".github/cms/docs/how_to_setup.md"
try:
    with open(documenation_file_contents, 'r') as f:
        documenation_file_contents = f.read()
        
        
except IOError:
    sys.exit('Documentation file does not exist, or has no content.  Exiting')

documentation_file_name = "pages/documentation.html"


output_from_parsed_template = documentation_template.render(menu=menu,Site_Name=Site_Name, AssetPath=AssetPath,documenation_file_contents=documenation_file_contents,footer_contents=footer_contents)

## Write out documenation.html file    
try:
    with open(documentation_file_name, 'w', encoding='utf-8') as fh:
        fh.write(output_from_parsed_template)
except IOError:
    sys.exit('Documentation template file does not exist, or has no content.  Exiting')  



########################################
#         End of  Documentation        #
########################################      
