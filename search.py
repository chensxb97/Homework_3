#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import math
import pickle
import os
from nltk.stem.porter import PorterStemmer

# python3 search.py -d dictionary.txt -p postings.txt  -q queries.txt -o results.txt


def usage():
    print("usage: " +
          sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")


def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below
    # Initialise stemmer
    stemmer = PorterStemmer()

    # Open and load dictionary
    # Sorted index dictionary is {term : [termID,docFrequency,charOffSet,strLength]}
    # Document length dictionary is {docID: cosine normalized document length}
    in_dict = open(dict_file, 'rb')
    sorted_dict = pickle.load(in_dict)
    sorted_index_dict = sorted_dict[0]
    docLengths_dict = sorted_dict[1]
    # Number of documents calculated for idf calculation
    number_of_documents = len(docLengths_dict)

    # Open posting lists, but not loaded into memory
    postings = open(postings_file, 'r')

    # Open queries file
    queries = open(queries_file, 'r')

    # Process queries ()
    # Create query_array = [{word: word frequency in query1},{word: word frequency in query2}...]
    query_array = []
    for line in queries:
        for sentence in nltk.sent_tokenize(line):
            query_dict = {}
            for word in nltk.word_tokenize(sentence):
                word = word.lower()
                word = stemmer.stem(word)
                if word in query_dict.keys():
                    query_dict[word] += 1
                else:
                    query_dict[word] = 1
            # Denominator for normalization of tf-idf (query)
            normalize_query = 0
            for word in query_dict.keys():
                # Calculate tf-wt
                q_tf = query_dict[word]
                q_tf_wt = 1 + math.log(q_tf, 10)
                # Calculate idf
                if word in sorted_index_dict.keys():
                    q_df = sorted_index_dict[word][1]
                    q_idf = math.log(number_of_documents/q_df, 10)
                else:
                    idf = 0
                q_wt = q_tf_wt * q_idf
                # Store wt for each word in query back into dictionary
                query_dict[word] = q_wt
                normalize_query += math.pow(q_wt, 2)
            # Calculate the cosine normalized value for query tf-idf
            for word in query_dict.keys():
                q_wt = query_dict[word]
                normalize_wt = q_wt/math.sqrt(normalize_query)
                query_dict[word] = normalize_wt

            print(query_dict)

            # Parse postings list for each word for valid documents which contains these words
            # Each document we will have an array of numbers for each word in the query
            document_dict = {}
            for word in query_dict.keys():
                if word in sorted_index_dict.keys():
                    termID = sorted_index_dict[word][0]
                    charOffset = sorted_index_dict[word][2]
                    strLength = sorted_index_dict[word][3]
                    postings.seek(charOffset, 0)
                    posting_str = (postings.read(strLength))
                    p_array = posting_str.split(',')
                    for p in p_array:
                        documentID = p.split('^')[0]
                        tf_raw = p.split('^')[1]
                        document_dict[documentID] = {}
                        document_dict[documentID][word] = tf_raw
                else:
                    pass

            normalize_doc = 0
            for document in document_dict.keys():
                for word in query_dict.keys():
                    if word in document_dict[document].keys():
                        d_tf = int(document_dict[document][word])
                        d_tf_wt = 1 + math.log(d_tf, 10)
                        document_dict[document][word] = d_tf_wt
                        normalize_doc += math.pow(d_tf_wt, 2)
                    else:
                        document_dict[document][word] = 0
                for word in query_dict.keys():
                    d_wt = document_dict[document][word]
                    d_normalize_wt = d_wt/math.sqrt(normalize_doc)
                    document_dict[document][word] = d_normalize_wt

            print(document_dict)

            query_array.append(query_dict)


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None:
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
