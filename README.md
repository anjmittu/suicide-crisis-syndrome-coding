
# suicide-crisis-syndrome-coding

This repository contains code for:

* Manual coding of keywords related to Suicide Crisis Syndrome (SCS) into categories associated with SCS (e.g. "no friends" -> Social Withdrawal),  and

* Automatically using the resulting keyword-to-category mapping to detect SCS-related categories in tet.

It assumes that clusters of related keywords have already been identified. (A separate codebase exists for doing this by identifying keywords that are statistically more likely in suicide-related text. It does this by comparing posts within and not-within r/SuicideWatch using the log-likelihood ratio with Dirichlet prior, followed by k-means clustering of the keywords' word2vec embeddings.)


## Setup

1. Pull this repo
   
2. Clone the kwic_ngrams repo
```
git submodule update --init
```

3. Install requirements
```
pip install -r requirements.txt
```

4. Add input data.  You need the cluster data, and reddit post files.  There should be two reddit post files,
   one with suicide watch posts and one with others.  These file paths are set in utils.
   
5. Create a directory for output.  This file path are set in utils.

## Creating coding spreadsheets

>   Author: Anjali Mittu
>
>   Take a set of keyword clusters like
>  
>     CLUSTERNAME, MAIN KEYWORD,  SCORE                        ,"OTHER KEYWORDS"
>     Cluster 40,       no friends,           13.617213991153418,"have no friends, no friends ,, no friends ., , no friends"
>  
>   and create an Excel spreadsheet suitable for coding and/or analysis.
>   It is currently specific -- in fact, hardwired -- for the specific
>   goal of creating coding spreadsheets for Reddit data. The clusters
>   are groups of keywords that appear statistically more frequently in
>   r/Suicidewatch and the coding is for criteria in Suicide Crisis Syndrome.


### Create KWIC lookup
```
python coding/build_kwic.py
```

### Create the spreadsheets
```
python coding/create_coding_file.py
```


## Using coded keywords to label text with SCS categories

>  Author: Jason Zhang, with modifications by Philip Resnik

Example (more documentation to be added):
```
python coding_text_with_categories.py --infile foo.in --codedfile SCS\ Keyword\ Pilot\ Coding_Combined.csv --clusterfile phrase_clusters_8K_3_minscore3_oneline.csv --outfile result.txt --include_coder Megan,Devon --primary_only
```


