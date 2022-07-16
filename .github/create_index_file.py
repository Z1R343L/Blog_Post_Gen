import codecs
# Open Index File
index_file_contents = ".github/index.md"
try:
    with open(index_file_contents, 'r') as f:
        index_file_contents = f.read()
        
        
except IOError:
    sys.exit('Input file does not exist, or has no content.  Exiting')

index_file_name = "index.html"
    
try:
    with codecs.open(index_file_name, 'w', encoding='utf-8') as f:
        f.write(f"""
        <header>
   <nav>
  

</nav>

      <h1>Simply Docs</h1>
 
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

