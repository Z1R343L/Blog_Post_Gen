 

if (window.location.href.indexOf("/pages/blog/search?") != -1) {

window.onload=function(){
     var url_string = window.location.href
      var url = new URL(url_string);
var c = url.searchParams.get("posts");
console.log(c);
     
      
     
     if (c === null){
document.body.innerHTML = "No search route provided"
       
     } else {
       
         const input = [

    {
url: "/Blog_Post_Gen/pages/blog/c_test_blog_post.html",
name: "Hello World 2",
contents: ","
published: "Test 0, 2020,"
},
    {
url: "/Blog_Post_Gen/pages/blog/blog_post_3.html",
name: "",
contents: ","
published: "2022-07-27,"
},
    {
url: "/Blog_Post_Gen/pages/blog/blog_post_1.html",
name: "Hello World",
contents: ","
published: "Test 1, 2020,"
},
    {
url: "/Blog_Post_Gen/pages/blog/test.html",
name: "",
contents: ","
published: "2022-07-27,"
},
    {
url: "/Blog_Post_Gen/pages/blog/jared.html",
name: "",
contents: ","
published: "2022-07-27,"
},
    {
url: "/Blog_Post_Gen/pages/blog/blog_post_2.html",
name: "Coool",
contents: ","
published: "Test 2, 2020,"
},
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
    

        
