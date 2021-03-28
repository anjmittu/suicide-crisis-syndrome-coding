import os
from collections import Counter
from spacy.lang.en import English

from kwic_ngrams.kwic import *
from utils import *


def create_corpus_for_kwic(corpusfile):
    """
    Reads in the r/SuicideWatch and other reddit posts and writes them to a file formatted for kwic code.

    :param corpusfile: The path to save the temporary corpus file
    """
    posts = []
    with open('../input/tokenized_sw_posts.txt', newline='') as sw_posts:
        posts.extend(sw_posts.readlines())
    with open('../input/tokenized_other_posts.txt', newline='') as other_posts:
        posts.extend(other_posts.readlines())

    posts = [post.replace('"', '') for post in posts]

    with open(corpusfile, "w", newline='') as all_posts:
        all_posts.writelines(posts)


def get_known_terms():
    """
    Creates a counter will all the key words and variations from the clusters.  This will format the phases for kwic
    by replacing spaces with underscores.

    :return: a counter will all the key words and variations from the clusters
    """
    known_terms = Counter()
    clusters = read_clusters_file()

    for cluster in clusters:
        known_terms[convert_string_for_kwic(cluster["keyword"])] = 1
        for term in split_variations(cluster["variations"]):
            if term:
                known_terms[convert_string_for_kwic(term)] = 1

    return known_terms


def create_contexts():
    """
    This will create a KWIC index file which can be read by another script.  Creates a temporary corpus file formated
    for kwic.  Loops through all the clusters to find all the key words and variations and creates an index
    with these phases.  This index file is writen to a file defined in utils.py
    """
    try:
        # Read in the reddit post and save them to a file for kwic
        create_corpus_for_kwic(CORPUS_FILE)

        # Get a counter with all the known terms.  Save this to a pickle file
        known_terms = get_known_terms()
        pickle.dump([known_terms, 0], open(COUNT_FILE, "wb"))

        # Initialize text processing
        logger.info("Initializing spacy")
        nlp = English(parser=False)  # faster init

        # Create the KWIC index
        os.remove(KWIC_FILE)
        logger.info("Creating KWIC index file {}".format(KWIC_FILE))
        create_kwic_index(nlp, CORPUS_FILE, COUNT_FILE, KWIC_FILE, window_width)
    finally:
        os.remove(CORPUS_FILE)
        os.remove(COUNT_FILE)


if __name__ == "__main__":
    create_contexts()
