"""
During my exploration of substring discovery, a few different techniques came to mind.  In
this file, I explore using different algorithms and data structures to solve the
problem.

All functions other than `_get_unique_sub_strings` are higher order functions.  They return a matching function 
that can be used to find which words exist in a substring.  I structured these different techinques
this way because I assume the set of words we're trying to find in URLs to be slowly or never
changing.  The higher order function will be called when the service/function is initialized,
for example before working on a batch of URLs or before a REST service is configured for use.

At runtime, the result of the higher order functions is called with the URL as the sole argument.

Each lower level matching function returns a frozenset containing the matched words.
"""
import re
import itertools

from flashtext import KeywordProcessor

from hunters_trie import Trie

def _get_unique_sub_strings(string):
    """
    Finds all the unique substrings in a given string.  For example, the
    string "apple" will return:
        a
        ap
        app
        appl
        apple
        p
        pp
        ppl
        pple
        p
        pl
        ple
        l
        le
        e
    This function is SLOW for long strings.  Small increases in string length can
    yield enourmous increases in returned set size thus increases in execution time.
    """
    return { string[i:j] for i in range(0, len(string)) for j in range(i+1, len(string)+1)}
                

def create_match_function_using_native(words):
    """
    Returns a function that takes in a `url` and returns the elements in `words`
    that are in `url`.  Does this using native Python substring lookup.
    """
    def match(url):
        return frozenset(word for word in words if word in url)
    return match


def create_match_function_using_set_intersection(words):
    """
    Returns a function that takes in a `url` and returns the elements in `words`
    that are in `url`.  Does this by, for each `url`, getting all the possible
    substrings within it and doing a set intersection with `words`. 
    """
    def match(url):
        return frozenset(_get_unique_sub_strings(url).intersection(words))
    return match


def create_match_function_using_trie(words):
    """
    Returns a function that takes in a `url` and returns the elements in `words`
    that are in `url`.  Does this by, creating a Trie with all the contents
    of `words` and for each `url`, getting all the substrings and returning
    those found in the Trie.  
    """
    # TODO: Explore is passing the iter to the trie class would be a faster way to add words into the Trie.  
    # Doesn't really matter because its a one time cost and paid at intialization time, not runtime.
    trie = Trie()
    for word in words:
        trie.add_word(word)
    def match(url):
        return frozenset(phrase for phrase in _get_unique_sub_strings(url) if trie.prefix_search(phrase))
    return match


def create_match_function_using_regex(words):
    """
    Returns a function that takes in a `url` and returns the elements in `words`
    that are in `url`.  Does this by using applying several large RegExs.  RegExs
    are created by:
        1. Seperating `words` into groups of the same character length.
        2. Creating RegEx matching patterns that look like `?=(word1|word2|...)`.
        3. Then applying the RegEx patterns of words of identicle length to `url`, capturing matches.
    We apply pattens containing words of the same length at the same time because of the nature of the nature
    of the patterns.
    For Example: If words is {"a", "mn", "b", "xyz"}, we'd create length_to_words_of_that_length as
    {1:["a","b"], 2:["mn"], 3:["xyz"]} and then patterns as [re.compile('?=(a|b)'), re.compile('?=(mn)'), 
    re.compile('?=(xyz)')].  At runtime, we'd then apply these patterns one at a time.  This type of 
    thing could be done in parallel! 

    This technique is faster than making a single regex expression for every word in `words`.
    """
    # This set up logic is a little confusing and could be written using comprehension expressions.
    d = {}
    for word in words:
        l = len(word)
        if l not in d:
            d[l] = []
        d[l].append(word)
    pattern_strings = ['(?=({}))'.format('|'.join(words_of_length_l)) for words_of_length_l in d.values()]
    patterns = [re.compile(p) for p in pattern_strings]
    def match(url):
        return frozenset({match for p in patterns for match in p.findall(url)})
    return match
