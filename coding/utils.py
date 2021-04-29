import csv
import logging as log

log.basicConfig(level=log.INFO)
logger = log.getLogger()

window_width = 11
CORPUS_FILE = '../input/temp_all_posts.txt'
KWIC_FILE = "../input/test_kwic_index.p"
COUNT_FILE = "../input/test_term_counts_file.p"
EXAMPLES_FILE = '../output_spreadsheets/examples.xlsx'
EXAMPLES_ONE_WORD_FILE = '../output_spreadsheets/examples_one_word.xlsx'
CODING_MULTI_WORD_FILE = '../output_spreadsheets/coding.xlsx'
CODING_ONE_WORD_FILE = '../output_spreadsheets/coding_one_word.xlsx'

cluster_data = []

contractions = [
    "ain't",
    "aren't",
    "can't",
    "can't've",
    "'cause",
    "could've",
    "couldn't",
    "couldn't've",
    "didn't",
    "doesn't",
    "don't",
    "hadn't",
    "hadn't've",
    "hasn't",
    "haven't",
    "he'd",
    "he'd've",
    "he'll",
    "he'll've",
    "he's",
    "how'd",
    "how'd'y",
    "how'll",
    "how's",
    "i'd",
    "i'd've",
    "i'll",
    "i'll've",
    "i'm",
    "i've",
    "isn't",
    "it'd",
    "it'd've",
    "it'll",
    "it'll've",
    "it's",
    "let's",
    "ma'am",
    "mayn't",
    "might've",
    "mightn't",
    "mightn't've",
    "must've",
    "mustn't",
    "mustn't've",
    "needn't",
    "needn't've",
    "o'clock",
    "oughtn't",
    "oughtn't've",
    "shan't",
    "sha'n't",
    "shan't've",
    "she'd",
    "she'd've",
    "she'll",
    "she'll've",
    "she's",
    "should've",
    "shouldn't",
    "shouldn't've",
    "so've",
    "so's",
    "that'd",
    "that'd've",
    "that's",
    "there'd",
    "there'd've",
    "there's",
    "they'd",
    "they'd've",
    "they'll",
    "they'll've",
    "they're",
    "they've",
    "to've",
    "wasn't",
    "we'd",
    "we'd've",
    "we'll",
    "we'll've",
    "we're",
    "we've",
    "weren't",
    "what'll",
    "what'll've",
    "what're",
    "what's",
    "what've",
    "when's",
    "when've",
    "where'd",
    "where's",
    "where've",
    "who'll",
    "who'll've",
    "who's",
    "who've",
    "why's",
    "why've",
    "will've",
    "won't",
    "won't've",
    "would've",
    "wouldn't",
    "wouldn't've",
    "y'all",
    "y'all'd",
    "y'all'd've",
    "y'all're",
    "y'all've",
    "you'd",
    "you'd've",
    "you'll",
    "you'll've",
    "you're",
    "you've"
]


def read_clusters_file():
    """
    This function reads the cluster data csv and saves each cluster as a dict with the keys `cluster_id`, `keyword`,
    and `variations`.  This should only read the cluster data once.  Once it has been read, it will used the saved
    list for future calls.

    :return: A list with each cluster dict
    """
    if not cluster_data:
        logger.info("Reading cluster data")
        with open('../input/phrase_clusters_8K_3_minscore3_oneline.csv', newline='') as csvfile:
            clusters = csv.reader(csvfile)
            for cluster in clusters:
                cluster_data.append({"cluster_id": cluster[0],
                                     "keyword": cluster[1],
                                     "variations": cluster[3]})
    return cluster_data


def split_variations(v):
    """
    Splits the variations string into a list of variation phrases.

    :param v: A string of variations
    :return: a list of variation phrases
    """
    v = v.split(", ")
    while "" in v:
        v.remove("")
    return v


def convert_string_for_kwic(string):
    """
    Prepares a string for kwic.  Replaces the spaces with underscores.

    :param string: The phrase
    :return: The same phrase with the spaces replaced with underscores
    """
    return string.replace(" ", "_")
