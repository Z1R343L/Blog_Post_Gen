import codecs

import re as regex
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.github/cms/layouts'))
template = env.get_template('documentation.html')
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

## Menu Settings File

permalinks_file= "navlinks.md"
permalinks_file_contents = None

## Get each link in file & add to menu
menu=""
pattern = 'Link:(.*?) New_Window:(.*?) Title:(.*?) Position:(.*?)'
with open(permalinks_file) as f:
  file_contents = f.read()
  for (link, window, title, position) in regex.findall(pattern, file_contents, regex.DOTALL):
    if window == "True":
      Open_New_Window = "__target blank"
    else:
      Open_New_Window = "__target blank"
    if link == "null":
      link = ""
    else:
      link = link
    menu += f"""<a href="{Asset_Path}{link}" {Open_New_Window}>{title}</a>"""  

# Open Index File Content
index_file_contents = ".github/cms/docs/how_to_setup.md"
try:
    with open(index_file_contents, 'r') as f:
        index_file_contents = f.read()
        
        
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')

index_file_name = "pages/documentation.html"


output_from_parsed_template = template.render(menu=menu, Asset_Path=Asset_Path,index_file_contents=index_file_contents)

# Write out index.html file    
try:
    with open(index_file_name, 'w', encoding='utf-8') as fh:
        fh.write(output_from_parse_template)
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')  
