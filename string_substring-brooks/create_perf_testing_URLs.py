import wikipedia
import random
import time

def create_dataset(size_of_dataset):
    """
    Produces a dataset of atleast size `size_of_dataset`.  Writes to ./perf_testing_URLs.txt.
    """
    start_time = time.time()
    pages = []
    print('Begining creation of a dataset of size >= {}.  This may take a bit...'.format(size_of_dataset))
    while len(pages) < size_of_dataset:
        for page_name in wikipedia.random(pages=10):
            try:
                pages.append(wikipedia.page(page_name, auto_suggest=True, redirect=True).url)
            except wikipedia.exceptions.WikipediaException:
                # Sometimes random articles are ambigious.  Skip these cases.
                continue
        print('Existing size:',len(pages))
    with open('./perf_testing_URLs.txt', 'w') as file_stream:
        file_stream.write('\n'.join(pages))
    print('took {} seconds to get {} random wikipedia URLs and create perf_testing_URLs.txt'.format(time.time() - start_time, len(pages)))


if __name__ == '__main__':
    create_dataset(100)