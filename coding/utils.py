import csv
import logging as log

log.basicConfig(level=log.INFO)
logger = log.getLogger()

window_width = 11
CORPUS_FILE = '../input/temp_all_posts.txt'
KWIC_FILE = "../input/test_kwic_index.p"
COUNT_FILE = "../input/test_term_counts_file.p"
EXAMPLES_FILE = '../output_spreadsheets/examples.xlsx'
CODING_FILE = '../output_spreadsheets/coding.xlsx'

cluster_data = []


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
