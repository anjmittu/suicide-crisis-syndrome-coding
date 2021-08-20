import xlsxwriter
from kwic_ngrams.kwic import *
from utils import *
import re

SIZE_OF_SHORT_COLUMN = 5
SIZE_OF_NORMAL_COLUMN = 15
SIZE_OF_LONG_COLUMN = 68
MAX_KW_EXAMPLES = 15


def get_max_variations(clusters):
    """
    This will return the max number of variations a cluster has.

    :param clusters: A list of clusters
    :return: The max number of variations
    """
    max_variations = 0
    for c in clusters:
        max_variations = max(max_variations, len(split_variations(c["variations"])))

    return max_variations


def get_keyword_examples(keywords, num_ex_per_kw, max_examples, kindex):
    """
    This creates a list of keyword in context examples for the given keywords.  Each keyword will have
    `num_ex_per_kw` amount of examples in the list.

    :param keywords: A list of keywords which examples should be created for
    :param num_ex_per_kw: The number of examples per keyword
    :param kindex: The kwic look up dict (from `read_kwic_index` output)
    :return: A list of kwic examples
    """
    examples = []
    for kw in keywords:
        kwic_string_list = kwic_query(kindex, convert_string_for_kwic(kw), window_width, True)
        examples.extend(kwic_string_list[:num_ex_per_kw])

    return examples[:max_examples]


def divide_cluster_words(clusters):
    """
    This divides the clusters in one word keywords and multi-word keywords

    :param clusters: The clusters to divide
    :return: A list of single word clusters and a list of multi-word clusters
    """
    single_words = []
    multi_words = []
    for cluster in clusters:
        cluster_words = re.sub('[^A-Za-z0-9\']+', ' ', cluster["keyword"]).split(" ")
        while '' in cluster_words:
            cluster_words.remove('')
        is_contraction = "".join(cluster_words).lower() in contractions or "'".join(cluster_words).lower() in contractions
        if len(cluster_words) == 1 or is_contraction:
            single_words.append(cluster)
        else:
            multi_words.append(cluster)

    return single_words, multi_words


def set_up_workbook(workbook, column_sizes, headings):
    """
    Sets up the workbook by setting the column sizes and the headers.

    :param workbook: The workbook object
    :param column_sizes: A dict mapping of execl column names to width sizes
    :param headings: A dict mapping of execl column names to header names
    :return: A worksheet with the column sizes and headers set
    """
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({
        'border': 1,
        'bg_color': '#C6EFCE',
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })

    for col in column_sizes.keys():
        worksheet.set_column(col, column_sizes[col])
    worksheet.set_row(0, 36)

    for header_pos in headings.keys():
        worksheet.write(header_pos, headings[header_pos], header_format)

    return worksheet


def add_coding_columns(worksheet, l):
    """
    Adding the columns for coding examples to the given worksheet

    :param worksheet: The worksheet to add the columns to
    :param l: The length of the worksheet
    """
    # Add columns for coding
    worksheet.data_validation(0, 2, l, 3, {'validate': 'list',
                                           'source': ['Entrapment', 'Affective Disturbance',
                                                      'Loss of Cognitive Control',
                                                      'Hyperarousal', 'Social Withdrawal', 'Suicidal Intent',
                                                      'Passive Suicidal Ideation', 
                                                      'Other relevant things that might indicate a suicidal crisis',
                                                      'None of the Above']})

    worksheet.data_validation(0, 4, l, 4, {'validate': 'list',
                                           'source': ['Very confident', 'Somewhat confident', 'Somewhat unsure',
                                                      'Very unsure']})

    worksheet.data_validation(0, 5, l, 5, {'validate': 'list',
                                           'source': ['Yes', 'No']})


def create_examples_sheet(clusters, workbook_name):
    """
    The function creates the examples spreadsheet.  For each cluster it lists the primary keyword, any variations,
    and examples of this cluster.

    :param workbook_name: The name of the spreadsheet
    :param clusters: A list of cluster objects
    """
    workbook = xlsxwriter.Workbook(workbook_name)
    headings = {"A1": "Item number", "B1": "Keyword", "D1": "Variations"}
    worksheet = set_up_workbook(workbook,
                                {'A:B': SIZE_OF_NORMAL_COLUMN, 'D:D': SIZE_OF_LONG_COLUMN},
                                headings)

    # Find the max number of variations to calculate the number of examples for each cluster
    max_variations = get_max_variations(clusters)
    logger.debug("The max variations: {}".format(max_variations))

    # Read KWIC index from a file
    logger.info("Reading KWIC index")
    kindex = read_kwic_index(KWIC_FILE)

    logger.info("Creating examples spreadsheet")
    # We start writing from row index 1
    sheet_ind = 1
    for i, cluster in enumerate(clusters):
        # Skip the header
        if i != 0:
            # The first line for the cluster has the cluster id, main keyword and variations
            worksheet.write_string(sheet_ind, 0, cluster["cluster_id"])
            worksheet.write_string(sheet_ind, 1, cluster["keyword"])
            worksheet.write_string(sheet_ind, 3, cluster["variations"])
            sheet_ind += 1

            # After this initial line we give examples for the cluster.  The keyword list has the main
            # keyword and all variations
            keywords = [cluster["keyword"]] + split_variations(cluster["variations"])
            # Calculate the number of examples per keyword
            # num_ex_per_kw = (max_variations + 1) * 3 // len(keywords)
            num_ex_per_kw = 3
            # Write each example to the spreadsheet
            for ex in get_keyword_examples(keywords, num_ex_per_kw, MAX_KW_EXAMPLES, kindex):
                worksheet.write_string(sheet_ind, 3, ex)
                sheet_ind += 1

    workbook.close()


def create_coding_sheet(clusters, workbook_name):
    """
    The function creates the examples spreadsheet.  For each cluster it lists the primary keyword, any variations.
    For each cluster a user can give a Primary Code, Secondary code, Confidence, and Flag for finer grained coding.

    :param workbook_name: The name of the spreadsheet
    :param clusters: A list of cluster objects
    """
    workbook = xlsxwriter.Workbook(workbook_name)
    headings = {"A1": "Item number",
                "B1": "Keyword",
                "C1": "Primary code (click cell for pull-down menu)",
                "D1": "Secondary code",
                "E1": "Confidence",
                "F1": "Flag for finer grained coding",
                "H1": "Variations"}
    column_sizes = {'A:F': SIZE_OF_NORMAL_COLUMN, 'G:G': SIZE_OF_SHORT_COLUMN,
                    'H:H': SIZE_OF_LONG_COLUMN}
    worksheet = set_up_workbook(workbook, column_sizes, headings)

    logger.info("Creating codings spreadsheet")
    for i, cluster in enumerate(clusters):
        # Skip the header
        if i != 0:
            # The line for the cluster has the cluster id, main keyword and variations
            worksheet.write_string(i, 0, cluster["cluster_id"])
            worksheet.write_string(i, 1, cluster["keyword"])
            worksheet.write_string(i, 7, cluster["variations"])

    add_coding_columns(worksheet, i)

    workbook.close()


def main():
    """
    Reads in the cluster data and creates the spreadsheets
    """
    clusters = read_clusters_file()
    single_words, multi_words = divide_cluster_words(clusters)

    create_examples_sheet(single_words, EXAMPLES_ONE_WORD_FILE)
    create_coding_sheet(single_words, CODING_ONE_WORD_FILE)

    create_examples_sheet(multi_words, EXAMPLES_FILE)
    create_coding_sheet(multi_words, CODING_MULTI_WORD_FILE)


if __name__ == "__main__":
    main()
