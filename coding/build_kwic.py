import os
import logging as log
from collections import Counter
from spacy.lang.en import English

from kwic_ngrams.kwic import *
from utils import *


def create_corpus_for_kwic(corpusfile):
    posts = []
    with open('../input/tokenized_sw_posts.txt', newline='') as sw_posts:
        posts.extend(sw_posts.readlines())
    with open('../input/tokenized_other_posts.txt', newline='') as other_posts:
        posts.extend(other_posts.readlines())

    posts = [post.replace('"', '') for post in posts]

    with open(corpusfile, "w", newline='') as all_posts:
        all_posts.writelines(posts)


def get_known_terms():
    known_terms = Counter()
    clusters = read_clusters_file()

    for cluster in clusters:
        known_terms[convert_string_for_kwic(cluster[1])] = 1
        for term in split_variations(cluster[3]):
            if term:
                print(convert_string_for_kwic(term))
                known_terms[convert_string_for_kwic(term)] = 1

    return known_terms


def create_contexts():
    try:
        create_corpus_for_kwic(corpusfile)

        known_terms = get_known_terms()
        pickle.dump([known_terms, 0], open(countfile, "wb"))

        # Initialize text processing
        log.info("Initializing spacy")
        nlp = English(parser=False)  # faster init

        # Create the KWIC index
        os.remove(kwicfile)
        log.info("Creating KWIC index file {}".format(kwicfile))
        create_kwic_index(nlp, corpusfile, countfile, kwicfile, window_width)
    finally:
        os.remove(corpusfile)
        os.remove(countfile)


def main():
    create_contexts()


if __name__ == "__main__":
    main()
