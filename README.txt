This is the README file for A0228375X-A0228420N's submission 
Email: 
e0673208@u.nus.edu (A0228375X)
e0673253@u.nus.edu (A0228420N)

== Python Version ==

We're using Python Version 3.7.4 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

The index dictionary is built by processing terms from the Reuters Training dataset. After removing all punctuation, case-folding all words to lower case and stemming, terms are stored in both a set (to ensure no duplicates) and a list (to track term frequencies), and are saved in the dictionary, sorted by term in ascending order, with the 
following format: {term: [termID, docFrequency, charOffset, stringLength]}.

- term(string) refers to the processed and stemmed word
- termID(int) is a unique ID associated with each word after the words have all been sorted in ascending order
- docFrequency(int) is the number of unique documents each term exists in
- charOffset(int) are character offset values which point to the start of the posting list in the postings file for that term.
- stringLength(int) states the length of the posting list generated for that term.

In addition to the index dictionary, we also keep track of the collection size by incrementing its value after processing each document. We also pre-compute the normalized
document lengths for each document and store them in a separate document lengths dictionary, with the following format: {docID: docLength}. The lengths are computed by taking 
the square root of the sum of squared (1+ log10(termFrequency)) for all unique terms in each document. These values will be used for cosine normalization of tf-idf weights in search.py. We also created a postings dictionary that stores the docId-termFrequency pairs for each term with the 
following format: {term: {docId: termFrequency}}. 

To build the postings file, we iterate through the terms from the postings dictionary and obtain each term's dictionary of docId-termFrequency pairs. We then construct the posting string using the value-pairs, with markers '^' to separate the docId and termFrequency and ',' to separate the pairs. After updating the charOffset and stringLength values in the main index dictionary, we write and save the posting strings to the output posting file.

Lastly, we save the finalised index dictionary, document lengths dictionary and collection size value as a list in a pickled file so that they could be easily re-loaded in memory to be used in search.py.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

The search algorithm takes in the pickled index dictionary, document lengths dictionary, collection size, postings file and queries file as input arguments.
The objective is to process each query and obtain the top K documents that are relevant to the query using the vector space model.

<TO BE FILLED>

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0228375X-A0228420N, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[] I, A0228375X-A0228420N, did not follow the class rules regarding homework
assignment, because of the following reason:

NIL

I suggest that I should be graded as follows:

NIL

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

<Please fill in>
