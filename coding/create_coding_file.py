import xlsxwriter
import logging as log

from kwic_ngrams.kwic import *
from utils import *


def get_max_variations(clusters):
    max_variations = 0
    for c in clusters:
        max_variations = max(max_variations, len(split_variations(c[3])))

    return max_variations


def get_keyword_examples(keywords, max_variations, kindex):
    examples = []
    num_ex_per_kw = (max_variations + 1) * 3 // len(keywords)
    for kw in keywords:
        kwic_string_list = kwic_query(kindex, convert_string_for_kwic(kw), window_width, True)
        examples.extend(kwic_string_list[:num_ex_per_kw])

    return examples


def create_examples_sheet(clusters):
    workbook = xlsxwriter.Workbook('../output_spreadsheets/examples.xlsx')
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({
        'border': 1,
        'bg_color': '#C6EFCE',
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })

    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('D:D', 68)
    worksheet.set_row(0, 36)

    headings = {"A1": "Item number", "B1": "Keyword", "D1": "Variations"}

    for header_pos in headings.keys():
        worksheet.write(header_pos, headings[header_pos], header_format)

    max_variations = get_max_variations(clusters)
    # Read KWIC index from a file
    log.info("Reading KWIC index")
    kindex = read_kwic_index(kwicfile)

    sheet_ind = 1
    for i, cluster in enumerate(clusters):
        # Skip the header
        if i != 0:
            worksheet.write_string(sheet_ind, 0, cluster[0])
            worksheet.write_string(sheet_ind, 1, cluster[1])
            worksheet.write_string(sheet_ind, 3, cluster[3])
            sheet_ind += 1
            for ex in get_keyword_examples([cluster[1]] + split_variations(cluster[3]), max_variations, kindex):
                worksheet.write_string(sheet_ind, 3, ex)
                sheet_ind += 1

    workbook.close()


def create_coding_sheet(clusters):
    workbook = xlsxwriter.Workbook('../output_spreadsheets/coding.xlsx')
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({
        'border': 1,
        'bg_color': '#C6EFCE',
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })

    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 5)
    worksheet.set_column('H:H', 68)
    worksheet.set_row(0, 36)

    headings = {"A1": "Item number",
                "B1": "Keyword",
                "C1": "Primary code (click cell for pull-down menu)",
                "D1": "Secondary code",
                "E1": "Confidence",
                "F1": "Flag for finer grained coding",
                "H1": "Variations"}

    for header_pos in headings.keys():
        worksheet.write(header_pos, headings[header_pos], header_format)

    for i, cluster in enumerate(clusters):
        # Skip the header
        if i != 0:
            worksheet.write_string(i, 0, cluster[0])
            worksheet.write_string(i, 1, cluster[1])
            worksheet.write_string(i, 7, cluster[3])

    worksheet.data_validation(0, 2, i, 3, {'validate': 'list',
                                           'source': ['Entrapment', 'Affective Disturbance',
                                                      'Loss of Cognitive Control',
                                                      'Hyperarousal', 'Social Withdrawal', 'Suicidal Intent',
                                                      'Other relevant things that might indicate a suicidal crisis',
                                                      'None of the Above']})

    worksheet.data_validation(0, 4, i, 4, {'validate': 'list',
                                           'source': ['Very confident', 'Somewhat confident', 'Somewhat unsure',
                                                      'Very unsure']})

    worksheet.data_validation(0, 5, i, 5, {'validate': 'list',
                                           'source': ['Yes', 'No']})

    workbook.close()


def main():
    clusters = read_clusters_file()
    create_examples_sheet(clusters)
    create_coding_sheet(clusters)


if __name__ == "__main__":
    main()
