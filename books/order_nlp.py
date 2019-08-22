import math
import time

import numpy as np

import spacy

nlp = spacy.load('en_core_web_md')

book_vectors = {}

def cosine_similarity(vec1, vec2):
    similarity = vec1.dot(vec2) / ((vec1 ** 2).sum() * (vec2 ** 2).sum())
    return similarity

def order_remaining_wishes(wished_books_list, all_books_list):
    """
    params:
        wished_books_list: an ordered list of books
        all_books_list: the list of all the books
    return:
        list of all book in order of preference
    """
    start_time = time.time()
    # weights for the books, the book with highest priority gets most weight
    weights = np.arange(2, 1, -1/len(wished_books_list))
    wished_books_vector = np.zeros((300,)) # spacy's word vector has shape (300,)
    # find the weighted average of all the vectors of the books name
    for i in range(len(wished_books_list)):
        wished_book = wished_books_list[i]
        doc = book_vectors.get(wished_book)
        if doc is None:
            doc = nlp(wished_book)
            book_vectors[wished_book] = doc
        wished_books_vector += weights[i] * doc.vector
    wished_books_vector /= np.sum(weights)

    # copy it, since we're going to change it
    new_all_books_list = all_books_list[:]
    for wished_book in wished_books_list:
        try:
            new_all_books_list.remove(wished_book)
        except Exception as e:
            print(e)
            # pass
            # print(wished_book, all_books_list)

    similarity_scores = []
    for i in range(len(new_all_books_list)):
        book = new_all_books_list[i]
        doc = book_vectors.get(book)
        if doc is None:
            doc = nlp(book)
            book_vectors[book] = doc

        similarity = cosine_similarity(wished_books_vector, doc.vector)
        similarity_scores.append((i, similarity))

    # some words may not be in the vocabulary so it may return NaN when
    # computing similarity; replace the score with zero
    for i in range(len(similarity_scores)):
        index, similarity = similarity_scores[i]
        if math.isnan(similarity):
            similarity_scores[i] = (index, 0.0)

    similarity_scores = sorted(similarity_scores,
                               key=lambda similarity: similarity[1],
                               reverse=True)

#     for similarity_score in similarity_scores:
#         i, similarity = similarity_score
#         print(new_all_books_list[i], similarity)

    scored_books_list = []
    for similarity_score in similarity_scores:
        index, similarity = similarity_score
        scored_books_list.append(new_all_books_list[index])

    end_time = time.time()
    print("Single similarity match time: ", end_time-start_time)
    return scored_books_list
