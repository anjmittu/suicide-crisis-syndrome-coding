# suicide-crisis-syndrome-coding
#
# This repository contains code that will take a set of keyword
# clusters like
#
#   CLUSTERNAME, MAIN KEYWORD,  SCORE                        ,"OTHER KEYWORDS"
#   Cluster 40,       no friends,           13.617213991153418,"have no friends, no friends ,, no friends ., , no friends"
#
# and create an Excel spreadsheet suitable for coding and/or analysis.
# It is currently specific -- in fact, hardwired -- for the specific
# goal of creating coding spreadsheets for Reddit data. The clusters
# are groups of keywords that appear statistically more frequently in
# r/Suicidewatch and the coding is for criteria in Suicide Crisis Syndrome.


## Set up
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

## Running code

### Create KWIC lookup
```
python coding/build_kwic.py
```

### Create the spreadsheets
```
python coding/create_coding_file.py
```
