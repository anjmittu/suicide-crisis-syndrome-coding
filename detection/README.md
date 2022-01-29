# Coding text with categories

The background for this is a collaboration with psychiatry folks in which we are looking for evidence of suicidal crisis in text.  Using a straighforward NLP approach, we have identified clusters of "keywords" (which contain multi-token phrases like `no friends` up to a limit of 3 tokens in length), and we are mapping those clusters to known categories related to potential suicidal crisis, e.g. Social Withdrawal or Affective Disturbance.

The goal for this piece of code is to take our information about clusters and categories, and use it to code/annotate text input.

## Inputs 

**coded\_clusters\_file:** a spreadsheet containing sets of manually coded keyword clusters, where the format is:

> CLUSTER_NUMBER, PRIMARY PHRASE, CODER1 PRIMARY, CODER1 SECONDARY, CODER2 PRIMARY, CODER2 SECONDARY, ...

for some number N of coders. For example (with N=2):

> Cluster 40,no friends,Social Withdrawal,Loss of Cognitive Control,Loss of Cognitive Control,Affective Disturbance, 
> 
> Cluster 51,my meds,Affective Disturbance,Loss of Cognitive Control,Loss of Cognitive Control,,

Notice that each coder can provide two codes, primary and secondary, although the secondary code can be empty (or equivalently "None of the Above").

**cluster\_info\_file:** a spreadsheet identifying the details of each cluster, e.g.:

> Cluster 40,no friends,13.61,"have no friends, no friends ,, no friends ., , no friends, no friends and, friends , no, . no friends, no real friends"
> 
> Cluster 51,my meds,9.47,"my medications, meds I take"

where the first column is the cluster number, the second column is the primary keyword for that cluster, the third column is a score, and the third column is a comma-separated list of alternative keywords. *(N.B. The third column was just a string for easy readability by human coders, but I need to change it to use a non-comma delimiter in between the keyword variants, for machine readability, since the keywords can contain commas!)*

**document\_file:** text containing one document per line.

## Options

Commandline flags make it possible to:

* Ignore secondary codes -- i.e. a boolean flag `--primary_only`. Default is to also use secondary codes. (See discussion below.)

* Identify names of coders to include (based on their name in the header line of the `coded_clusters_file`) -- i.e. a multi-valued commandline option like `--include_coder=Megan,Devon`. Default is to include all coders.

* Use scores instead of counts -- i.e. a flag `--use-scores`. (See discussion below.)

## What the program does

### Basic operation

For each document (line) in `document_file`, tokenize using SpaCy, and produce a count of how many matches there are *for each code*. For example, if the input is:

> I have no friends, or at least no real friends, nobody to help keep me on my meds.

then with `--primary_only` we have matches on Social Withdrawal and Loss of Cognitive Control (via Cluster 40, keywords `no friends` and `no friends ,` and `no real friends`) and we also have matches on Affective Disturbance and Loss of Cognitive Control (via Cluster 51, keyword `my meds`). So the output would be:

> Loss of Cognitive Control:2, Social Withdrawal:1, Affective Disturbance:1

where Loss of Cognitive Control has a count of 2 because there were matches for two different clusters that led to that code.  (Notice a cluster is considered either matched or not matched, even if there are multiple keywords that occur, e.g. this sentence contains both `no friends` and `no real friends`, but Cluster 40 is only considered to match once.

### Using secondary codes

If the `--primary_only` flag were not set, then we could also pay attention the secondary codes for Clusters 40 and 51. In this case, for Cluster 40 we now add a match for Affective Disturbance (Coder 2's secondary code for that cluster), so the result for this input line would instead be:

> Loss of Cognitive Control:2, Social Withdrawal:1, Affective Disturbance:1

### Using scores

If `--use_scores` were set, then when we go from keyword matches to clusters to codes, we take the score for the cluster into account, summing up the total score for each code instead of a count.  For the above example (returning to `--primary_only`), when Cluster 40 is matched via the multiple variations of `no friends`, that provides a bump up of 13.61 for the scores for the associated codes Social Withdrawal and Loss of Cognitive Control.  And when Cluster 51 is matched via `my meds`, that provides a bump up of 9.47 for the associated codes Affective Disturbance and Loss of Cognitive Control.  So now the value for Loss of Cognitive Control in the output line would not be 2, it's 13.61+9.47=23.08. 

### Lining up the output with the input

The output should contain a blank line if no categories matched, so that the output file has exactly the same number of lines as the input.  That way a simple `paste` command can be used to associate each output with the input line it belongs to.








