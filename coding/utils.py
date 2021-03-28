import csv
import logging as log

window_width = 11
corpusfile = '../input/temp_all_posts.txt'
kwicfile = "../input/test_kwic_index.p"
countfile = "../input/test_term_counts_file.p"

cluster_data = []


def read_clusters_file():
    if not cluster_data:
        log.info("Reading cluster data")
        with open('../input/phrase_clusters_8K_3_minscore3_oneline.csv', newline='') as csvfile:
            clusters = csv.reader(csvfile)
            for cluster in clusters:
                cluster_data.append(cluster)
    return cluster_data


def split_variations(v):
    v = v.split(", ")
    while "" in v:
        v.remove("")
    return v


def convert_string_for_kwic(string):
    return string.replace(" ", "_")
