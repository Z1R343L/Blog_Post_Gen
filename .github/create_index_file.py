import codecs
# Open Index File
index_file_contents = ".github/index.md"
try:
    with open(index_file_contents, 'r') as f:
        index_file_contents = f.read()
        
        
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')

    
try:
    with codecs.open(file_name, 'w', encoding='utf-8') as f:
        f.write(f"""{index_file_contents}""")
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')  
