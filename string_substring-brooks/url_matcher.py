"""
Background:
Assume you are designing a performance application to match keywords found in a url. What data structures / technologies would you employ to ensure a speedy (sub 10ms) algorithm that is able to match substrings against the URL? To help shape your thinking, let's assume that were dealing with a finite subset of words. This may help bound which algorithms would be most applicable for this problem. 

Please also provide an actual code sample. Always helpful to see a running example but obviously doesn't need to be ready for production. 

Please zip the contents of your solution named: `string_substring-[lastname].zip`
--------
Handle set up problems in functions that evaluate ish
--------
I'm assuming during the match we need to know which words we matched to.
A lot of work could be done during a set up phase before actually doing matches.
Run in parallel.
"""
import time
import re
import random
import itertools

from trie import HuntersTrie


def preprocess_words(words):
    """
    Does some light preprocessing on a collection of words:
        -   Removes single character words
        -   Converts all words to containing only lower case characters
        -   removes words with any non-letter in them, like punctuation 
    """
    return {word.lower() for word in words if len(word) > 1 and word.isalpha()}


def load_words(file_name):
    """
    Returns the contents of `file_name` as a set for O(const) lookup.
    """
    with open(file_name) as file_stream:
        words = file_stream.read().split('\n')
    # Newlines at the end of files cause an empty string to be in `words`.  When this happens, remove it:
    if '' in words:
        words = words[:-1]
    return preprocess_words(set(words))
    

def helper_to_be_renamed(url_string):
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


def test_performance(words, function_to_name_mapping):
    pass   
                

def create_match_using_native(words):
    def match(url):
        return {word for word in words if word in url}
    return match


def create_match_using_set_intersection(words):
    def match(url):
        # TODO: See if switching these helps.  It shouldnt..
        return words.intersection(helper_to_be_renamed(url))
    return match


def create_match_using_trie(words):

    # TODO: Explore is passing the iter to the trie class would be a faster way to add words into the Trie.  Doesn't really matter becayse its a one time cost. 
    trie = HuntersTrie()
    for word in words:
        trie.add_word(word)

    def match(url):
        return {phrase for phrase in helper_to_be_renamed(url) if trie.prefix_search(phrase)}

    return match


def create_match_using_regex(words):
    """
    if words = {a, b, ab}
    we create {1:{a,b}, 2:{ab}}
    """
    unique_lengths_of_all_words = {len(word) for word in words}
    length_to_words_of_that_length = {length: set() for length in unique_lengths_of_all_words}
    for word in words:
        length_to_words_of_that_length[len(word)].add(word)
    patterns = []
    for length in sorted(length_to_words_of_that_length.keys()):
        patterns.append(re.compile(''.join([
            '(',
            '|'.join(length_to_words_of_that_length[length]),
            ')'
        ])))

    def match(url):
        result = []
        for pattern in patterns:
            result.extend(pattern.findall(url))
        return result

    return match


def test_functionality(name_to_function_mapping):
    """
    Though not a substitue for production grade Behave tests, this funciton
    tests to make sure my the matching functions operate as expected.
    """
    TEST_CASES = [
        {
            'url': 'www.apple.com',
            'expected_words': sorted(['app', 'apple'])
        },
        {
            'url': 'www.facebook.com',
            'expected_words': sorted(['book', 'face'])
        },
        {
            'url': 'www.linkedin.com',
            'expected_words': sorted(['ink', 'link'])
        },
    ]
    for function_name in sorted(name_to_function_mapping.keys()):
        func = name_to_function_mapping[function_name]
        for test_case in TEST_CASES:
            url = test_case['url']
            expected_words = test_case['expected_words']
            result = sorted(func(url))
            if result != expected_words:
                error_string = '''{function_name} didn't return the expected words in {url}
                Expected: {expected_words}
                Found: {found_words}
                '''.format({
                    'function_name': function_name,
                    'url': url,
                    'expected_words': expected_words,
                    'found_words': result,
                })
                raise ValueError(error_string)

def main():

    # word_source = '/usr/share/dict/words' # TODO: Make configurable.
    # word_source = './words.txt' # From: https://github.com/first20hours/google-10000-english/blob/master/20k.txt
    word_source = './nouns.txt' # From: http://www.desiquintans.com/downloads/nounlist/nounlist.txt

    words = load_words(word_source)
    print('\nThe number of unique words in {}:'.format(word_source), len(words))
    print('A subset of the words:', ', '.join(random.sample(words, 5)))


    method_name_to_method_matching_function = {
        'regex_match': create_match_using_regex(words),
        'trie_match': create_match_using_trie(words),
        'native_python': create_match_using_native(words),
        'native_set_intersection': create_match_using_set_intersection(words)
    }
    
    test_functionality(method_name_to_method_matching_function)
    print('\nFunctional tests passed.')


if __name__ == '__main__':
    main()