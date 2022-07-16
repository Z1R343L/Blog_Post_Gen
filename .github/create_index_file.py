import codecs
#with open(index_template_file) as f:
 # index_template = f.read() 


# Open Index File
index_file_contents = ".github/index.md"
try:
    with open(index_file_contents, 'r') as f:
        index_template = f.read()
        
        
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')

index_file_name = "index.html"
    
try:
    with codecs.open(index_file_name, 'w', encoding='utf-8') as f:
        f.write(f"""{index_template}""")
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')  
