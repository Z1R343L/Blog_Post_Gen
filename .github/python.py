#! /usr/bin/env python
# -*- coding: utf-8 -*-

########################################
#              Import(s)               #
########################################    

import codecs
import sys
import re
import os
import requests
import json
import time
import html
import subprocess
import platform
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import datetime
from jsmin import jsmin
import pytz
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

## Robots.Txt Disallow Links
robots_txt_disallow = "" 

## Page Slugs
page_slugs = ""


########################################
#          End of Lists(s)             #
########################################    








########################################
#            Function(s)               #
########################################    

## Function to get all files in directory & sub-folders

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If Directory Exists - Make File If Not Ignore File Name Used.
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


import re


# Define Emoji Data To Use
EmojiData = {
	"yum": "😋 ",
	"heart": "sd",
	"s": "delectus aut autem",
	"ad": "false"
}
    
        
# Function to Parse & Replace Emojis With Image Or Unicode


# Example of usage (text, replace types = Unicode, Image, class name for images)
 
	# Replace with image URL (JSON data) & add css class 
#print(ParseEmoji("<script> so dam :yum: :yum: :heart: </script>", "Image", "my_class_name"))	
  
	 # Replace with unicode emoji (JSON data)
#print(ParseEmoji("<script> so dam :yum: :yum: :heart: </script>"))	

def ParseEmoji(text, type=None, Class=None):
    # Regex to remove HTML from string
    Text_With_Any_HTML_Removed = re.compile(r'<.*?>')
    # Remove all HTML from string
    Text_With_Any_HTML_Removed= Text_With_Any_HTML_Removed.sub('',text)
    # For all regex matches of :VALUE: in text
    for Regex_Match in re.findall(':(.*?):', Text_With_Any_HTML_Removed):
        # For each key name in JSON Emoji Data
        for Key_Name in EmojiData.items():
            # if Regex Match is a Keyname
            if Regex_Match in EmojiData:
                # Replace with the Keyname Value
                if type == "Image":
                    if Class:
                        text = text.replace(f':{Regex_Match}:', str(f'<img class="{Class}" src="{EmojiData[Regex_Match]}">'))
                    else:
                        text = text.replace(f':{Regex_Match}:', str(f'<img src="{EmojiData[Regex_Match]}">'))
                else:
                    text = text.replace(f':{Regex_Match}:', str(EmojiData[Regex_Match])) 
    return text
            
        
        

## Function to get File Creation Dates
# https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
def creation_date(path_to_file, blog_date_format):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    
    Default blog date format is  -- '%d, %b %Y'
    
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        try:
          # file creation timestamp in float
          Date = os.path.getctime(path_to_file)
          Post_Time = datetime.datetime.fromtimestamp(Date, pytz.timezone('US/Eastern')).strftime(blog_date_format)
          return Post_Time
        except AttributeError:
          # file modification timestamp of a file
          Date = os.path.getmtime(path_to_file)
          Post_Time = datetime.datetime.fromtimestamp(Date, pytz.timezone('US/Eastern')).strftime(blog_date_format)
          return Post_Time




## Function to create breadcrumbs


# TODO - add settings file for breadcrumb links
## Option to set element + create class
def generate_bc(homepage_url, url):
    separator = " "
    if '//' in url:
        url = url[url.index('//') + 2:]

    url = url.rstrip('/')

    try:
        for i, c in enumerate(url):
            if c in ['?', '#']:
                url = url[0:i]
                break

        menus = url.split('/')[1:]
        if menus and 'index.' == menus[-1][0:6]:
            menus = menus[:-1]
        if not menus:
            return '<li class="active">HOME</li>'

        breadcrumb = f'<li><a href="{homepage_url}">HOME</a></li>'

        for i, e in enumerate(menus[:-1]):
            breadcrumb += separator + f'<li><a href="{homepage_url}/' +'{}/">{}</a></li>'.format('/'.join(menus[:i + 1]), get_element_name(e))

        breadcrumb += separator + '<li aria-current="active">{}</li>'.format(get_element_name(menus[-1]))
        return breadcrumb
    except:
        return url



## Not really a clue what this is for 
ignore_words = ["the", "of", "in", "from", "by", "with", "and", "or", "for", "to", "at", "a"]


def get_element_name(element):
    acronyms = element.split('-')
    for i, c in enumerate(acronyms[-1]):
        if c == '.':
            acronyms[-1] = acronyms[-1][:i]
            break

    if len(element) > 30:
        for i, c in reversed(list(enumerate(acronyms))):
            if c in ignore_words:
                acronyms.pop(i)
        return ''.join([s[0].upper() for s in acronyms])

    return ' '.join([s.upper() for s in acronyms])


########################################
#          End of Function(s)          #
########################################    











########################################
#           SITE SETTINGS              #
########################################    


## Set the time zone

est = pytz.timezone('US/Eastern')
utc = pytz.utc

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


try:
  Site_URL = var['Site_URL']
except:
  print("You need to have a site URL defined in your settings.md file, exiting...")
  sys.exit()


	

if var['Blog_Post_Date_Format']:
  blog_date_format = var['Blog_Post_Date_Format']
else:
  blog_date_format= '%d, %b %Y'




## Check if hosted on GitHub
  ### To Run Git Commands If True (For pushing commits etc)
if var['GitHub_Hosted']:
  GitHub_Hosted = var['GitHub_Hosted']
else:
  GitHub_Hosted = "False"
	
	

## Open Emoji Parser settings file
settings_file = ".github/emoji_parser.md" 
with open(settings_file, 'r') as f:
  for line in f:
   ## Make JSON Key Values
   if ":" in line:
    name, value = line.split('=================END OF SETTINGS============')[0].split(':')  
    var[name] = str(value).rstrip()   
  globals().update(var)


	
if var['Parse_Emojis'] == "True":
  Parse_Emojis = True
  try:
   Emoji_Class = var['Emoji_Class']
  except:
   Emoji_Class = None
  try:
   Emoji_Type = var['Emoji_Type']
  except:
   Emoji_Type = None
else:
  Parse_Emojis = False
	
	




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
#             Create Pages             #
########################################    


## Create pages (not including blog route pages) 

content = {}
var = {}
dirName = ".github/cms/custom_pages"

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
    try:
      PagePath = data["PagePath"]
    except:
      PagePath = "pages/"   


    outputFolder = PagePath
    os.makedirs(outputFolder, exist_ok=True)
    file_name = outputFolder + Path(file).stem + ".html"  

	
    # Create Breadcrumbs	
    try:
      CreateBreadCrumbs = data["Breadcrumbs"]
      if CreateBreadCrumbs == "True":
        BreadCrumbs = generate_bc(f'https://{Site_URL}{AssetPath}', f'https://{Site_URL}{AssetPath}{outputFolder}{Path(file).stem}.html')
        print(BreadCrumbs)
      else:
        BreadCrumbs = None
    except:
      BreadCrumbs = None


    # For writing JSON data for github.com/MarketingPipeline/Static-Search.js
    json_data += """{url: """ + f'"{AssetPath}{PagePath}{file_name}",\n' + "name: " +f'"{PageTitle}",\n' + "contents: " + '"ADD PAGE CONTENTS", \n ' + "published: " + '"ADD PUBLISHED DATE",\n' +  "type: " + '"page",\n' + "},"
	

    # Create page slug 
    try:
      PageSlug = data["PageSlug"]
      page_slugs += f'if (document.location == "https://{Site_URL}{PageSlug}" || document.location == "http://{Site_URL}{PageSlug}")' + "{" + f'window.location.href = "http://{Site_URL}{PageSlug}/{Path(file).stem}"' + "}"
    # pass if no page slug found to make  
    except:
      pass  


    try:
      PageLayout = data["PageLayout"]
    except:
      PageLayout = "custom_page_default.html"      
    page_template = env.get_template(PageLayout)
    try:
        with open(file_name, 'w') as fh:
          page_template = page_template.render(Site_Name=Site_Name,menu=menu,SiteTitle=SiteTitle,PageTitle=PageTitle,Facebook_Meta=Facebook_Meta,AssetPath=AssetPath, BreadCrumbs=BreadCrumbs, footer_contents=footer_contents)	
          fh.write(page_template)
	    
    except IOError:
        sys.exit(u'Unable to write to files: {0}'.format(file_contents))  
    var.clear()
    content.clear()




########################################
#          End of Create Pages         #
########################################    

	












########################################
#               BLOG                   #
########################################      

# TODO - add a function to turn blog ON / OFF

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
      Robots_Index = data["Robots_Index"]
      if Robots_Index == "False":
        robots_txt_disallow += "User-agent: *\nDisallow:" + outputFolder + Path(file).stem 
    except:
      pass



    try:
      SiteTitle = data["SEO_Title"]
    except:
      SiteTitle = "Blog Post"


    try:
      BlogDate = data["BlogDate"]
    except:
      BlogDate= creation_date(file, blog_date_format)


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
url: """ + f'"{AssetPath}{file_name}",\n' + "name: " +f'"{BlogTitle}",\n' + "contents: " + f'"{BlogDescription}",\n' + "published: " + f'"{html.unescape(BlogDate)}",\n' + "},"
	
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
# Check line for <meta name="robots" content="noindex">, etc
        if re.search("<meta\s+name.+robots.+content.+noindex", line):
	        robots_txt_disallow += Path(file).stem 
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

# TO DO - add function to turn search route on or off.

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
search_file_name = "assets/js/blog-search.min.js"
try:
    with codecs.open(search_file_name, 'w', encoding='utf-8') as f:
       # minify the JS file
        minified = jsmin(""" 

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
        f.write(minified)
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
      # Testing Emoji Parser
	      if Parse_Emojis == True:
                documenation_file_contents = ParseEmoji(f.read(),Emoji_Type,Emoji_Class)
	      else:
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









########################################
#           Robots.txt File            #
########################################    

template = env.get_template('robots.txt')

robots_file_name = "robots.txt"
output_from_parsed_template = template.render(robots_txt_disallow=robots_txt_disallow)

try:
    with open(robots_file_name, 'w') as fh:
        fh.write(output_from_parsed_template)
except IOError:
    sys.exit('Robots.txt layout does not exist, or has no content.  Exiting')  

########################################
#        End Of Robots.txt File        #
########################################    	

















########################################
#              Page Slugs              #
########################################    

## Create Page Slugs JS file
page_slugs_file_name = "assets/js/page-slugs.min.js"
try:
    with codecs.open(page_slugs_file_name, 'w', encoding='utf-8') as f:
       # minify the JS file
        minified = jsmin(page_slugs)
        f.write(minified)
except Exceptation as e:
    print(e)  

########################################
#           End of Page Slugs          #
########################################    










########################################
#             Minify Assets            #
########################################    

dirName = ".github/cms/layouts/assets/"

for file in getListOfFiles(dirName):
  with open(file, 'r') as f:
    ## These are used for below	
    path=os.path.dirname(file)
    print(file)
    file_path = os.path.basename(path)	
    ## Minify JS Files
    if Path(file).suffix == ".js":
      js_file = f.read()
      minified_js = jsmin(js_file)
      if file_path == "assets":
        JS_FileName = "assets/" +  Path(file).stem + ".min.js"
      else:
        JS_FileName = "assets/" + path.split("assets/")[1]  + "/" +  Path(file).stem + ".min.js"
        print(JS_FileName)
      JS_File = open(JS_FileName, "w")
      JS_File.write(minified_js)
      JS_File.close()
    ## Minify CSS Files
    if Path(file).suffix == ".css":
      # Open file		
      css_text = f.read()
      f.close()
      ## Send API request for minified CSS	
      r = requests.post("https://www.toptal.com/developers/cssminifier/api/raw", data={"input":css_text})
      css_minified = r.text
     
       ### Check if file path contains anything after /assets/  	   
      if file_path == "assets":
	      Output_Folder = "assets/" 
      else:   
	      ### File path contains something after /assets/ + adding path. 
	      Output_Folder = "assets/" + path.split("assets/")[1]  + "/"
      
      file_name = Output_Folder + Path(file).stem + ".min.css"
      CSS_File = open(file_name, "w")
      CSS_File.write(css_minified)
      CSS_File.close()
    else:
      ## Copy all files from .github/assets/ to /assets/	
      ### Don't copy un-minified JS files
      if Path(file).suffix == ".js":
	      break
      ### Don't copy un-minified CSS files
      if Path(file).suffix == ".css":
	      break
      ### Copy & move all the other files to /assets/ folder. 
      ### Check if file path contains anything after /assets/  	   
      if file_path == "assets":
	      Output_Folder = "assets/" + os.path.basename(file)
      else:   
	      ### File path contains something after /assets/ + adding path. 
	      Output_Folder = "assets/" + path.split("assets/")[1]  + "/" + os.path.basename(file)
      shutil.copyfile(file, Output_Folder)

## Optimize all images in assets path
command = """optimize-images ./assets/"""
ret = subprocess.run(command, capture_output=True, shell=True)
    
	
########################################
#             Minify Assets            #
########################################    
	
	
	
	
	
	
	
	
	
	
	
	

########################################
#           Sitemap Generator          #
########################################   

# To do - add another try statement here and except error that python command is not found

## Run the sitemap generator
try:
    ## Try to see if Python is avaliable on system
    command = """python .github/generate_sitemap.py"""
    ret = subprocess.run(command, capture_output=True, shell=True)
except:
    # If not try Python 3 (I am sure there is a better method of detection for this) 	
    command = """python3 .github/generate_sitemap.py"""
    ret = subprocess.run(command, capture_output=True, shell=True)


########################################
#        End of Sitemap Generator      #
########################################   
	
	
	
	
	
	
	
	
	
	
	
	
	

########################################
#            Commit Changes            #
########################################   

if GitHub_Hosted == "True":
    ## Commit changes to CMS content (pages / posts / minifed CSS & JS)	
    command = """git config --global user.name "github-actions[bot]"; git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"; git add -A; git commit -m "Updated CMS Content" ; git push"""
    ret = subprocess.run(command, capture_output=True, shell=True)
else:
    print("No changes found to create for CMS")


########################################
#          End of Commit Changes       #
########################################   
