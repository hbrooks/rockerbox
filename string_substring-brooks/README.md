### Problem Text:
Background:
Assume you are designing a performance application to match keywords found in a url. What data structures / technologies would you employ to ensure a speedy (sub 10ms) algorithm that is able to match substrings against the URL? To help shape your thinking, let's assume that were dealing with a finite subset of words. This may help bound which algorithms would be most applicable for this problem. 

Please also provide an actual code sample. Always helpful to see a running example but obviously doesn't need to be ready for production. 

Please zip the contents of your solution named: `string_substring-[lastname].zip`


### Assumptions:
- The words we're trying to find in URLs changes slowly or not at all.  Because of this, I don't need to create the data strutures, like this for example, used in the higher order `matching_methods.py` functions each time a substring lookup is evaluated.  I can do some "set up" work before returning a function to handle the matches. 
- We need to know which words in the word source are in the URL, not only that at least one word from the word source is in the URL.
- 



### Structure:
In order to explore the best ... I tried many


### Deploying as a Web Service:
When designing this app, I had in mind the use case where as URLs come into some backend system, they need to be tagged based on set of words.  Deploying one of the functions in `matching_methods.py` as a AWS Lambda/GCP CloudFunction would be easy and creates a "tagging" microservice.  The elastic nature of those services handles most scability concerns, except bursty traffic, well.  My concerns would be about the size of the word source.  Those products operate on low memory, and if we can't load the word source into a gigabyte or so we'd have a problem.  To investigate, I check the size of a largest, easy to access word source, `/usr/share/dict/words`:
```
>>> with open('/usr/share/dict/words') as fs:
...     text = fs.read()
>>> words = text.split()
>>> len(words)
235886
>>> from sys import getsizeof
>>> getsizeof(words)
2007112
```
`getsizeof` returns sizes in bytes so a collection of about a quarter million words is only 2 MB.  Therefore, space isn't much of a concern.

If our word source did have millions of words, we could shard the source and run the "tagging" service in parallel for each shard.  At execution time, we'd wait for each service to finish looking for words, using it's shard as the word source.  Then, we'd return the words found across all services.  


### Batch


### Drawbacks of my Approaches

### The Word Source
I found the most interesting results when using a list of nouns I found from [this](http://www.desiquintans.com/downloads/nounlist/nounlist.txt) site as the source of words I am to find in URLs.  I also explored using the `/usr/share/dict/words` file on my MacOS but opted against it because I got several odd words I had never heard of.  For example, when using `/usr/share/dict/words` as the word source for the URL `www.google.com/search?q=how-old-is-the-earth`, the results set is 
```
how,earth,old,sear,ow,ar,ear,search,ea,og,art,se,arch,sea,om,goo,ogle,go,arc,he,th,the,is,ho
```
which has a whole bunch of words, like "ea", I've never heard of...  For comparison, when using `nouns.txt`, the result set is the more standard english friendly set of
```
earth,arch,art,ear,sea,search
```
Running the functional tests with anything other than `./nouns.txt` throws an error.


