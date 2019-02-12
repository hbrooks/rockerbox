import re
import itertools

from hunters_trie import Trie


def _helper_to_be_renamed(url_string):
    """
    apple
    --
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
    """
    return { url_string[i:j] for i in range(0, len(url_string)) for j in range(i+1, len(url_string)+1)}
                

def create_match_using_native(words):
    def match(url):
        return {word for word in words if word in url}
    return match


def create_match_using_set_intersection(words):
    def match(url):
        # TODO: See if switching these helps.  It shouldnt..
        return words.intersection(_helper_to_be_renamed(url))
    return match


def create_match_using_trie(words):
    # TODO: Explore is passing the iter to the trie class would be a faster way to add words into the Trie.  Doesn't really matter becayse its a one time cost. 
    trie = Trie()
    for word in words:
        trie.add_word(word)
    def match(url):
        return {phrase for phrase in _helper_to_be_renamed(url) if trie.prefix_search(phrase)}

    return match


def create_match_using_regex(words):
    """
    if words = {a, ab, b, xyz}
    we create length_to_words_of_that_length={1:[a,b], 2:[ab], 3:[xyz]}
    then patterns = [re.compile('(a|b)'), re.compile('(ab)'), re.compile('(xyz)')]
    """
    d = {} # This all could be done in one or two comprehension expressions, but is kept longer for clarity.
    for word in words:
        l = len(word)
        if l not in d:
            d[l] = []
        d[l].append(word)
    pattern_strings = ['(?=({}))'.format('|'.join(d[l])) for l in sorted(d.keys())]
    patterns = [re.compile(p) for p in pattern_strings]
    
    def match(url):
        return {match for p in patterns for match in p.findall(url)}

    return match