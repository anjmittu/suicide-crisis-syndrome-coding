# pip install en_core_web_sm-3.1.0.tar.gz

import spacy
import pandas as pd
from nltk import ngrams
from collections import defaultdict
import argparse
from tqdm import tqdm
from parameters import *
import sys



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', default=None,
                            help='Input text to process, one raw text unit per line')
    parser.add_argument('--codedfile', default=None,
                            help='CSV file: clusters coded into SCS categories')
    parser.add_argument('--clusterfile', default=None,
                            help='CSV file: cluster keywords and variants')
    parser.add_argument('--outfile', default=None,
                            help='Output one line per input line')
    parser.add_argument('--primary_only', default=False, action='store_true',
                            help='Use only primary SCS category codings, not secondary')
    parser.add_argument('--include_coder', default=None,
                            help='Coders to include, defaults to all of them')
    parser.add_argument('--use_scores', default=False, action='store_true',
                            help='Use cluster scores rather than counts in output')
    parser.add_argument('--include_unigrams', default=None, action='store_true',
                            help='Allow text/keyword matching with unigrams, defaults to false')
    args = parser.parse_args()

    if (args.infile is None or args.codedfile is None or args.clusterfile is None or args.outfile is None):
        sys.exit("Required arguments: --infile, --codedfile, --clusterfile, --outfile. Use --help to see all commandline parameters.\n")

    if (args.include_coder is None):
        args.include_coder = ",".join(valid_coders)
    print("Using coders: {}".format(args.include_coder))
        
    return args


def check_coder(include_coder):
    # Print a warning if the input coder name is not in the coder list
    for coder in args.include_coder.split(','):
        if coder not in valid_coders:
            print(f'Warning: the input name is not a valid coder. Please check again.')


def read_doc(file, nlp, include_unigrams=False):
    # Read the document sample, use SpaCy to process the document
    result = []
    raw_lines = []
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in tqdm(lines, desc='Read doc'):
            line_ngram = []
            line = line.strip()
            if not line:
                continue

            temp = []
            for word in nlp(line):
                # Lowercase
                temp.append(str(word).lower()) 
            if (include_unigrams):
                # Unigrams not included by default since they tend to overgenerate
                for item in ngrams(temp, 1):
                    line_ngram.append(' '.join(item))
            for item in ngrams(temp, 2):
                line_ngram.append(' '.join(item))
            for item in ngrams(temp, 3):
                line_ngram.append(' '.join(item))
            result.append(line_ngram)
            raw_lines.append(line)

    return result, raw_lines


def read_code_and_cluster(code, cluster):
    # Read the two tables: code & cluster. Notice there are special characters utf8 can't handle
    code = pd.read_csv(code, encoding='Latin-1')
    cluster = pd.read_csv(cluster, encoding='Latin-1')
    
    return code, cluster


def split_variants(text):
    # Replace the double comma with simple comma, and deduplicate
    # The input is a string and the output is a list of deduplicated string
    # NOTE: this treatment of double commas is a bit of a kludge for the
    # particular instance of the input file being used to develop the code.
    # In future, the input format will change so that the input text
    # for this routine will use '||' as the delimiter for variants.
    text = text.replace(',,', ',')
    text = list(set([i.strip() for i in text.split(',')]))
    
    return text


def get_variants(cluster, target_clu):
    # Get the variant list from the cluster table
    for idx in cluster.itertuples():
        keyword = getattr(idx, 'Keyword').strip()
        curr_clu = getattr(idx, 'Cluster').strip()
        variants = getattr(idx, 'Variants')
        
        if pd.isna(variants):
            variants = []
        else:
            # Here to split the string into a text and deduplicate
            variants = split_variants(variants.strip())
        
        # If the cluster_id is matched, then return all variants and keyword itself in a list
        if curr_clu == target_clu:
            new_variants = [keyword]
            new_variants.extend(variants)
            new_variants = list(set(new_variants))
            
            return new_variants


def filter_code(code, primary_only, include_coder=None):
    # Filter the code table based on the options
    columns = code.columns.to_list()

    # We don't need to iterate on the keyword and cluster_id columns
    new_columns = columns[:2]
    for column in columns[2:]:
        if primary_only:
            # If the primary_only is true, keep the column if it's primary
            if '- P' in column:
                # If the include_user contains value, keep the column if the name is in the wanted list
                if include_coder is not None:
                    if column.split()[0] in include_coder.split(','):
                        new_columns.append(column)
                # If the includer_user is None, just keep the column
                else:
                    new_columns.append(column)
        
        else:
            if include_coder is not None:
                if column.split()[0] in include_coder.split(','):
                    new_columns.append(column)
            else:
                new_columns.append(column)

    code = code[new_columns]
    return code


def process(args, lines, raw_lines, cluster, code, output_file='result.txt'):
    outf = open(output_file, 'w', encoding='utf8')
    for line, raw_line in tqdm(zip(lines,raw_lines), desc='Process doc', total=len(lines)):
        # Reset for a new line of text
        matched_clusters= []
        score = 0
        dic = defaultdict(int)

        print("\n-----\n")
        print("DEBUG: Processing line: {}".format(raw_line))
        
        # Notice here we iterate the code table instead of the cluster table
        # This is just to keep consistency when we match code with labels        
        for idx, _ in enumerate(list(code['Keyword'])):
            clu = list(code['Cluster'])[idx]
            variants = get_variants(cluster, clu)
            # print(" DEBUG: Considering idx={}, clu={}, variants={}".format(idx,clu,variants))

            # This is just to be safe, in case there are duplicate clusters in the data
            if clu in matched_clusters:
                continue
            
            # Iterate through all the variants, the keyword itself is included in it.
            for var in variants:
                if var not in line:
                    continue

                # Iterate through the valid columns in the coders' assigment of primary/secondary codes,
                # and add the labels to the dictionary
                for column in code.columns.to_list()[2:]:
                    if not pd.isna(list(code[column])[idx]) and \
                                str(list(code[column])[idx]) != 'None of the Above':
                        if args.use_scores:
                            dic[list(code[column])[idx]] += float(list(cluster['Score'])[idx])
                        else:
                            dic[list(code[column])[idx]] += 1
                        print(" DEBUG: variant '{}' matched {} (score {}) --> {}".format(
                            var,
                            clu,
                            round(float(list(cluster['Score'])[idx]),2),
                            list(code[column])[idx]))
                        break # If it matched any coder, no need to consider other coders
                matched_clusters.append(clu)

                break

            # Put together results with match counts (or scores)
            result = []
            if dic:
                sorted_dic = sorted(dic.items(), key = lambda kv: kv[1], reverse=True) # sort descending by count/score
                for k, v in sorted_dic:
                    result.append(f'{k}:{v}')
                    
        # Write the counts/scores per category. If there is no match in the line, there will be blank line 
        outf.write(f'{", ".join(result)}\n')

        print("DEBUG: Result = {}".format(result))
            
    outf.close()


if __name__ == '__main__':

    args = parse_args()

    if args.use_scores and args.primary_only:
        print(f'Warning: use_scores option will overwrite primary_only if used together.')

    # It is frustrating to get the wrong result just because of a typo in the name, 
    # This will throw out a warning if the name can't be found in a hardcord name list.
    check_coder(args.include_coder)

    # Set up and read in the files. 
    # The coded_clusters_file is named "code" and the cluster_info_file is named "cluster" for simplicity
    nlp = spacy.load('en_core_web_sm')
    lines, raw_lines = read_doc(args.infile, nlp, args.include_unigrams)
    code, cluster = read_code_and_cluster(args.codedfile, args.clusterfile)

    # Filter the code table based on the options
    if not args.use_scores:
        code = filter_code(code, args.primary_only, args.include_coder)

    # Process the document and output to a text file named result 
    process(args, lines, raw_lines, cluster, code, args.outfile)
