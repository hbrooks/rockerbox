### Structure of Submission:
I really enjoyed this assingment!  My solution is probably more involved than the average submission, but I had fun thinking about the best way to find substrings using Python3.  To get a quick result, run `python evaluate_methods.py` and read only this section.

Before settling on a best solution, I explored a few different approaches.  For each appraoch, I perform functional (unit) tests to make sure the logic of those implementions is sound and performance tests to gauge which are the fastest algorithms.  

Found in `matching_methods.py`, my considered solutions are:
- Using native Python substring. Example: `sub_string in string`.  I considered Python's `string.find()` method, but it seems that it should be used when we need to get the index of a substring.
- Using Regular Expressions. I created large matching patterns from the words in the word source, then used non-greedy matching to find the matches. 
- Using Set Intersection.  Faster than a list's O(N) lookup, set's provide constant order look up because they hash elements.  I leveraged this by creating a set of all the possible string combinations in a URL and doing a speedy set intersection between a set of the words in the word source and the string combinations in the URL. 
- Using a Trie.  I created a Trie data structure in `hunters_trie.py` and use it to do prefix lookup of each of the possible string combinations in the URL.  It could be improved in a few ways, one of which is by using ASCII string integer values instead of their string values. 

Exact details of each method can be found in the appropriate function in `matching_methods.py`.

All the matching functions take in a single URL as their argument.  The time on average to match a URL would be lower if they consumed an iterable of URLs, but I kept it this way because I imagine this app being some sort of "tagging" microservice that works on individual URLs at run time.  

I dont use any forms of parallel computing anywhere.  This could seriously speed up things, like the regex pattern evaluation!

It's worth noting that there are plenty of more advanced substring finding algorithms that we could apply based on the details of how long the URL is and how long each word we're trying to scan for is.  Rabin-Karp and Knuth-Morris-Prat come to mind.

Thanks for investigating my submission!


### Assumptions:
- The word source changes slowly or not at all.  
  - Because of this, I feel comfortable using higher order functions in `matching_methods.py` to set up data structures used in the returned functions.  This set up logic does not execute at run
time and instead happens only once when the matching function is created.
- We need to know which words in the word source are in the URL, not only that at least one word from the word source is in the URL.
- We care about words from any part of the URL, including the `www`'s, `.com`'s, and anything in the path.
  - For example `tail` should be in the result set of `captailone` despite `tail` not being what a human might say is a logical "word" in that example.
  - It wouldn't be hard to apply a preprocessing function to strip `www.` and `.com/*`-like phrases if we only care about some of the URL.



### Running Code:
My submission requires only standard Python libraries.

To run the functional and performance tests, please use `python evaluate_methods.py`. 

Please run all scripts from the `string_substring-brooks/` folder!


### The Word Source:
I found the most interesting results when using a list of nouns as the word source.  I got that list from [this](http://www.desiquintans.com/downloads/nounlist/nounlist.txt) site.  I also explored using the `/usr/share/dict/words` file on my MacOS but opted against it because I got several odd words I had never heard of.  For example, when using `/usr/share/dict/words` as the word source for the URL `www.google.com/search?q=how-old-is-the-earth`, the results set is 
```
how,earth,old,sear,ow,ar,ear,search,ea,og,art,se,arch,sea,om,goo,ogle,go,arc,he,th,the,is,ho
```
which has a whole bunch of words, like "ea", I've never heard of.  For comparison, when using `nouns.txt`, the result set is the more friendly set of
```
earth,arch,art,ear,sea,search
```

I do some light preprocessing on the words from the word source.  See that logic in the `preprocess_words` function of `evaluate_methods.py`.


### URL Source used in Performance Testing:
I couldn't for the life of me find a robust source of "random" URLs.  Kaggle had no related datasets and numerous Google searches didn't turn up anything good.  I was able to create a dataset using Wikipedia's Random Page functionality [(link)](https://en.wikipedia.org/wiki/Wikipedia:Random).

The script `perf_testing_URL.txt` creates a random performance testing dataset using the handy Wikipedia library.  You don't need to run this script because I've included it's artifact, `perf_testing_URLs.txt`. But you certainly can create a new one!  If you'd like to create a new performance testing list, you'll probably need to `pip install wikipedia`.  To run my script that creates `perf_testing_URL.txt`, please run `python create_perf_testing_URLs.py`.

The generated performance testing URL isn't perfect because all the pages are from Wikipedia and special characters are Base64 encoded, but it'll do.  Some example entries:
```
https://en.wikipedia.org/wiki/Jump_shot_(basketball)
https://en.wikipedia.org/wiki/National_Hobo_Association
https://en.wikipedia.org/wiki/Little_League_Baseball
https://en.wikipedia.org/wiki/Gri%C5%A1k%C4%81ni_Parish
https://en.wikipedia.org/wiki/Director_of_FSB
https://en.wikipedia.org/wiki/Quarantine_(Laurel_Halo_album)
```


### Results:
A sample output of `python evaluate_methods.py` is:
```
Average performance:
 - regex_match: 1.2074170204309316 ms
 - trie_match: 1.3061502805122962 ms
 - native_python: 0.5330975239093487 ms
 - native_set_intersection: 0.23875351135547349 ms
```
My Trie is the slowest!  There are no doubt optimizations to be made in my Trie.  I wasn't surpised that the Regex approach was slow because the matching patterns I've defined are enormous and executed in serial.  Native Python is suprisingly speedy, but not faster than set intersection.  Because the hashing of all sub strings from the URLs is cost effective (relatively short strings), this approach is quick, despite there being lots of substrings.

However, all the results are an order of magnitude less than the 10 ms we were aiming for!


### Functional Tests:
These are far from production ready, but service their purpose.  This app would be a great application for Behave (GivenWhenThen) tests.  Running `python evaluate_methods.py` executes the functional tests.

Running the functional tests with anything other than `./nouns.txt` as the word source throws an error.




### Deploying as a Web Service:
When designing this app, I had in mind the use case where URLs coming into some backend system  need to be tagged.  Deploying one of the functions in `matching_methods.py` as a AWS Lambda/GCP CloudFunction would be easy and creates a "tagging" microservice.  The elastic nature of those services handles most scability concerns well, except very bursty traffic.  My concerns would be about the size of the word source.  Those products operate on low memory, and if we can't load the word source into a gigabyte or so we'd have a problem.  To investigate, I check the size of a large, easy to access word source, `/usr/share/dict/words`:
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
`getsizeof` returns sizes in bytes, so a collection of about a quarter million words is only 2 MB.  Therefore, space isn't much of a concern and traffic consistency becomes the primary issue.

If our word source did have millions of words, we could shard the source and run the "tagging" service in parallel for each shard.  At execution time, we'd wait for each service to finish looking for words, using it's shard as the word source.  Then, we'd return the words found across all services.  


### Deploying as Batch Functionality
This tool could also be deployed as a function applied to URLs in a batch process!  The process to put this into an Apache Beam PTransformation would be to just create a wrapper around the setup function.

