# suicide-crisis-syndrome-coding

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