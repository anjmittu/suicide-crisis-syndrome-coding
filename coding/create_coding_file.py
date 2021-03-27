import xlsxwriter
import logging as log

from kwic_ngrams.kwic import *
from utils import *


def create_examples_sheet():
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

    clusters = read_clusters_file()
    for i, cluster in enumerate(clusters):
        # Skip the header
        if i != 0:
            worksheet.write_string(i, 0, cluster[0])
            worksheet.write_string(i, 1, cluster[1])
            worksheet.write_string(i, 3, cluster[3])

    workbook.close()


def create_coding_sheet():
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

    clusters = read_clusters_file()
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


def create_contexts():
    # Read KWIC index from a file
    log.info("Reading KWIC index")
    kindex = read_kwic_index(kwicfile)

    kwic_string_list = kwic_query(kindex, "i_think_i", window_width, True)
    for kwic_string in kwic_string_list[:3]:
        print(kwic_string)



def main():
    create_examples_sheet()
    create_coding_sheet()
    create_contexts()


if __name__ == "__main__":
    main()
