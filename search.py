#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import math
import pickle
import os
import time
from nltk.stem.porter import PorterStemmer
from heapq import nlargest


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
    # Collection size: Total number of documents, to be used for idf calculation
    in_dict = open(dict_file, 'rb')
    sorted_dict = pickle.load(in_dict)
    sorted_index_dict = sorted_dict[0]
    docLengths_dict = sorted_dict[1]
    collection_size = sorted_dict[2]

    # Open posting lists, but not loaded into memory
    postings = open(postings_file, 'r')

    # Open queries file
    queries = open(queries_file, 'r')

    # Store the results for each query
    # query_results = [[result for query1],[result for query 2]...]
    query_results = []
    for query in queries:
        for sentence in nltk.sent_tokenize(query):
            # Store all normalized query tf-idf weights in query_dict
            query_dict = process_query(
                sentence, sorted_index_dict, collection_size, stemmer)

            # Store all normalized document tf weights in document_dict
            document_dict = process_documents(
                query_dict, sorted_index_dict, postings)

            # Generates the top 10 documents for the query
            scores = process_scores(query_dict, document_dict, docLengths_dict)

            query_results.append(scores)

    # Write results into given results_file
    with open(results_file, 'w') as results_file:
        for result in query_results:
            # If result is empty, just write an empty line
            # If result is not empty, write each documentID (starting from highest rank) with a whitespace separating each documentID
            if result is not None:
                for index, (docID, score) in enumerate(result):
                    results_file.write(docID)
                    results_file.write(' ')
            results_file.write('\n')
    print('done!')


def process_query(input_query, sorted_index_dict, collection_size, stemmer):
    query_dict = {}
    for word in nltk.word_tokenize(input_query):
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
        q_tf_wt = 1 + math.log10(q_tf)
        # Calculate idf
        if word in sorted_index_dict.keys():
            q_df = sorted_index_dict[word][1]
            q_idf = math.log10(collection_size/q_df)
        else:
            q_idf = 0
        q_wt = q_tf_wt * q_idf
        # Store wt for each word in query back into dictionary
        query_dict[word] = q_wt
        normalize_query += math.pow(q_wt, 2)
    if normalize_query == 0:
        return None
    # Calculate the cosine normalized value for query
    for word in query_dict.keys():
        q_wt = query_dict[word]
        normalize_wt = q_wt/math.sqrt(normalize_query)
        query_dict[word] = normalize_wt

    return query_dict


def process_documents(query_dictionary, sorted_index_dict, input_postings):
    # document_dict = {document1: {word1: tf1, word2: tf2}, document2:{}...}
    if query_dictionary == None:
        return None
    document_dict = {}
    for word in query_dictionary.keys():
        if word in sorted_index_dict.keys():
            charOffset = sorted_index_dict[word][2]
            strLength = sorted_index_dict[word][3]
            input_postings.seek(charOffset, 0)
            posting_str = (input_postings.read(strLength))
            posting_array = posting_str.split(',')
            for p in posting_array:
                documentID = p.split('^')[0]
                tf_raw = p.split('^')[1]
                if documentID not in document_dict.keys():
                    document_dict[documentID] = {}
                document_dict[documentID][word] = int(tf_raw)
        else:
            pass
    for document in document_dict.keys():
        for word in query_dictionary.keys():
            if word in document_dict[document].keys():
                d_tf = int(document_dict[document][word])
                # Calculate tf-wt
                d_tf_wt = 1 + math.log10(d_tf)
                # Store tf-wt for each word in document back into dictionary
                document_dict[document][word] = d_tf_wt
            else:
                document_dict[document][word] = 0

    return document_dict


def process_scores(query_dictionary, document_dictionary, docLengths_dict):
    if query_dictionary == None:
        return None
    result = []
    for docID in document_dictionary.keys():
        # Denominator for normalization of tf-idf (docLength)
        normalize_doc = docLengths_dict[int(docID)]
        docScore = 0
        for term in query_dictionary.keys():
            doc_wt = document_dictionary[docID][term]
            term_wt = query_dictionary[term]
            docScore += doc_wt*term_wt
        # Normalizing the cosine product value with the docLength
        docScore /= normalize_doc
        result.append((docID, docScore))
    # Use heapq library 'nlargest' function to return top 10 results in O(10logn) time instead of sorting the entire array which would be O(nlogn) time
    return nlargest(10, result, key=lambda x: x[1])


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
