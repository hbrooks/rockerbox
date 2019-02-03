import time


def test():
    """
    Though not a substitute for production grade Behave tests, this function
    runs some quick unit and performance tests on the critical `match()` function.
    """ 
    words = load_words()
    trie_of_words = interpret_words_into_trie()
    tests = load_tests() # Each test needs: url, id, correct_result,
    test_start_time = time.time()
    responses = {test['id']: match(test['url'], trie_of_words) for test in tests}
    test_end_time = time.time()
    print('Ran {n_tests} tests in {test_duration} seconds'.format(
        {
            'n_tests': len(tests),
            'test_duration': test_end_time-test_start_time
        }
    )
    incorrect_tests = [test['id'] for test_id, response in responses.items()]


def match():
    pass

if __name__ == '__main__':
    pass