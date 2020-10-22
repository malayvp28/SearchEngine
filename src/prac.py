from functools import reduce
import sys
import math
from collections import defaultdict
import tkinter as tk

root = tk.Tk()

canvas1 = tk.Canvas(root, width=1000, height=500,  relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Search Engine')
label1.config(font=('helvetica', 14))
canvas1.create_window(500, 25, window=label1)

label2 = tk.Label(root, text='Enter your Query:')
label2.config(font=('helvetica', 10))
canvas1.create_window(500, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(500, 140, window=entry1)


# Document Corpus
document_filenames = {0: "C:/Users/Pruthvi/Desktop/IRS/17bit077_p4/Swift.txt",
                      1: "C:/Users/Pruthvi/Desktop/IRS/17bit077_p4/xcent.txt",
                      2: "C:/Users/Pruthvi/Desktop/IRS/17bit077_p4/tuv.txt",
                      3: "C:/Users/Pruthvi/Desktop/IRS/17bit077_p4/hondacity.txt"
                      }
# The size of the corpus
N = len(document_filenames)

# dictionary: a set to contain all terms (i.e., words) in the document
# corpus.
dictionary = set()

postings = defaultdict(dict)


document_frequency = defaultdict(int)


length = defaultdict(float)


characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"


def main_t():
    initialize_terms_and_postings()
    initialize_document_frequencies()
    initialize_lengths()
    # while True:
    x1 = entry1.get()
    first = do_search(x1)
    label3 = tk.Label(root, text=' search  ' +
                      x1 + ' is:', font=('helvetica', 10))
    canvas1.create_window(500, 210, window=label3)
    label4 = tk.Label(root, text=first, font=('helvetica', 10, 'bold'))
    canvas1.create_window(500, 230, window=label4)


def initialize_terms_and_postings():
    """Reads in each document in document_filenames, splits it into a
    list of terms (i.e., tokenizes it), adds new terms to the global
    dictionary, and adds the document to the posting list for each
    term, with value equal to the frequency of the term in the
    document."""
    global dictionary, postings
    for id in document_filenames:
        f = open(document_filenames[id], 'r', encoding='utf8')
        document = f.read()
        f.close()
        terms = tokenize(document)
        unique_terms = set(terms)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
            postings[term][id] = terms.count(term)  # the value is the
            # frequency of the
            # term in the
            # document


def tokenize(document):
    """Returns a list whose elements are the separate terms in
    document.  Something of a hack, but for the simple documents we're
    using, it's okay.  Note that we case-fold when we tokenize, i.e.,
    we lowercase everything."""
    terms = document.lower().split()
    return [term.strip(characters) for term in terms]


def initialize_document_frequencies():
    """For each term in the dictionary, count the number of documents
    it appears in, and store the value in document_frequncy[term]."""
    global document_frequency
    for term in dictionary:
        document_frequency[term] = len(postings[term])


def initialize_lengths():
    """Computes the length for each document."""
    global length
    for id in document_filenames:
        l = 0
        for term in dictionary:
            l += imp(term, id)**2
        length[id] = math.sqrt(l)


def imp(term, id):

    if id in postings[term]:
        return postings[term][id]*inverse_document_frequency(term)
    else:
        return 0.0


def inverse_document_frequency(term):

    if term in dictionary:
        return math.log(N/document_frequency[term], 2)
    else:
        return 0.0


def do_search(query):
    stry = ''

    #query = tokenize(input("Search query >> "))
    query = tokenize(query)
    if query == []:
        sys.exit()
    # find document ids containing all query terms.  Works by
    # intersecting the posting lists for all query terms.
    relevant_document_ids = intersection(
        [set(postings[term].keys()) for term in query])
    if not relevant_document_ids:
        stry = stry+'No documents matched all query terms.'
    else:
        scores = sorted([(id, similarity(query, id))
                         for id in relevant_document_ids],
                        key=lambda x: x[1],
                        reverse=True)
        stry = stry+'Score: filename\n'
        for (id, score) in scores:
            stry = stry+str(score)+": "+document_filenames[id]+"\n"
    return stry


def intersection(sets):

    return reduce(set.intersection, [s for s in sets])


def similarity(query, id):

    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*imp(term, id)
    similarity = similarity / length[id]
    return similarity


button1 = tk.Button(text='Search ', command=main_t,
                    bg='green', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(500, 180, window=button1)

root.mainloop()
