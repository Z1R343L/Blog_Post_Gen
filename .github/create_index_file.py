import codecs

import re as regex


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

if var['Site_Name']:
  Site_Name = var['Site_Name']
else:
  Site_Name = ""

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
    menu += f"""{position}<a href="{link}" {Open_New_Window}>{title}</a>"""  

# Open Index File Content
index_file_contents = ".github/index.md"
try:
    with open(index_file_contents, 'r') as f:
        index_file_contents = f.read()
        
        
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')

index_file_name = "index.html"
    
# Write out index.html file    
try:
    with codecs.open(index_file_name, 'w', encoding='utf-8') as f:
        f.write(f"""
        <head>
         <meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Home | {SiteName}</title>
  
<meta name="description" content="A showcase of Simply Docs by MarketingPipeline built using Simple.CSS">

<link rel="stylesheet" href="./assets/style.css">
</head>
        
        <header>
   <nav>
  {menu}

</nav>

      <h1>{SiteName}</h1>
 
    </header>
<main>

{index_file_contents}
</main>
<a href="https://github.com/MarketingPipeline/Simply-Docs/archive/refs/heads/main.zip"><button>Download This Template</button></a>



<footer>
      <p>Simply Docs was created by <a href="https://github.com/MarketingPipeline/">Marketing Pipeline</a> and is licensed under the MIT license.</p>
  <small>© 2014 Some company name</small>
      <address>email@email.com</address>
    </footer>
   
 <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/markdown-tag.js"></script> 
        """)
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')  

