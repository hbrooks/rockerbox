import time
import random


from matching_methods import create_match_function_using_native
from matching_methods import create_match_function_using_regex
from matching_methods import create_match_function_using_set_intersection
from matching_methods import create_match_function_using_trie


def load_words(file_name):
    """
    Returns the contents of `file_name` as a frozenset for constant order lookup.
    """
    with open(file_name) as file_stream:
        words = file_stream.read().split('\n')
    # Newlines at the end of files cause an empty string to be in `words`.  When this happens, remove it:
    if '' in words:
        words = words[:-1]
    return frozenset(preprocess_words(words))
   
    
def preprocess_words(words):
    """
    Does some light preprocessing on a collection of words:
        -   Removes single character words
        -   Converts all words to containing only lower case characters
        -   removes words with any non-letter in them, like punctuation 
    """
    return {word.lower() for word in words if len(word) > 1 and word.isalpha()}


def test_functionality(name_to_function_mapping, word_source):
    """
    Though not a substitue for production grade Behave tests, this funciton
    tests to make sure my the matching functions operate as expected.
    """
    if word_source not in ['./nouns.txt']:
        raise NotImplementedError('\nAt the moment, functional tests are only supported when using nouns.txt as the word source.')

    TEST_CASES = [
        {
            'url': 'www.apple.com',
            'expected_words': frozenset({'app', 'apple'})
        },
        {
            'url': 'www.facebook.com',
            'expected_words': frozenset({'book', 'face'})
        },
        {
            'url': 'www.linkedin.com',
            'expected_words': frozenset({'ink', 'link'})
        },
        {
            'url': 'www.google.com/search?q=how-old-is-the-earth',
            'expected_words': frozenset({'earth','arch','art','ear','sea','search'})
        },
    ]
    for function_name in sorted(name_to_function_mapping.keys()):
        for test_case in TEST_CASES:
            url = test_case['url']
            expected_words = test_case['expected_words']
            func_result = name_to_function_mapping[function_name](url)
            if func_result != expected_words:
                error_string = '''{function_name} didn't return the expected words for "{url}"
                Expected: {expected_words}
                Found: {found_words}
                '''.format(
                    function_name=function_name,
                    url=url,
                    expected_words=','.join(expected_words),
                    found_words=','.join(func_result),
                )
                raise ValueError(error_string)


def test_performance(name_to_function_mapping):
    """
    Returns a dictionaries containing information about the average matching
    time in miliseconds of each of the items in name_to_function_mapping.  Assumes
    the perf_testing_URLs.txt file exists!
    """
    n_trails = 5 # How many samples of performance on the urls to measure.
    with open('./perf_testing_URLs.txt') as file_stream:
        urls = file_stream.read().split('\n')
    average_trail_times = {}
    for name, matching_function in name_to_function_mapping.items():
        average_trail_times[name] = []
        for _ in range(n_trails):
            start_time = time.time()
            for url in urls:
                matching_function(url)
            end_time = time.time()
            average_trail_times[name].append((end_time-start_time)/len(urls))
    return {name: (sum(data)/n_trails)*1000. for name, data in average_trail_times.items()}
    

def main():
    # TODO: Make this a CLI prompt.
    word_source = './nouns.txt' # From: http://www.desiquintans.com/downloads/nounlist/nounlist.txt
    # word_source = '/usr/share/dict/words'

    words = load_words(word_source)
    print('\nThe number of unique words in {}:'.format(word_source), len(words))
    print('A subset of the words:', ', '.join(random.sample(words, 5)))

    # Create the matching functions!
    method_name_to_method_matching_function = {
        'regex_match': create_match_function_using_regex(words),
        # 'trie_match': create_match_function_using_trie(words),
        # 'native_python': create_match_function_using_native(words),
        # 'native_set_intersection': create_match_function_using_set_intersection(words)
    }
    
    test_functionality(method_name_to_method_matching_function, word_source)
    print('\nFunctional tests passed.')

    print('\nAverage performance:')
    for name, time in test_performance(method_name_to_method_matching_function).items():
        print(' - {}: {} ms'.format(name, time))


if __name__ == '__main__':
    main()