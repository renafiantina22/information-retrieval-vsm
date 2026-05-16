# ========IMPORT LIBRARY=======
import sys
import math
import string

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# ==========MEMBACA ARGUMENT COMMAND LINE=========
base_file = sys.argv[1]
query_file = sys.argv[2]

print("Base file:", base_file)
print("Query file:", query_file)


# ========MEMBACA QUERY=======
with open(query_file, "r") as f:
    query = f.read()

print("\nIsi query:")
print(query)


# ========MEMBACA DAFTAR DOKUMEN========
with open(base_file, "r") as f:
    docs = f.read().splitlines()

print(docs)


# =======MEMBACA ISI SEMUA DOKUMEN======
documents = {}

for doc in docs:
    with open(doc, "r") as f:
        documents[doc] = f.read()

#print(documents)


# =========INISIALISASI==========
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


# =========FUNGSI PREPROCESSING==========
def preprocess(text):

    # lowercase
    text = text.lower()

    # tokenisasi
    tokens = word_tokenize(text)

    # hapus stopword dan tanda baca
    filtered = []

    for word in tokens:
        if word not in stop_words and word not in string.punctuation:
            filtered.append(word)

    # stemming
    stemmed = []

    for word in filtered:
        stemmed.append(stemmer.stem(word))

    return stemmed


# ==========PREPROCESSING DOKUMEN===========
processed_docs = {}

for doc in documents:
    processed_docs[doc] = preprocess(documents[doc])

#print(processed_docs)


# ========MENGHITUNG TF (TERM FREQUENCY)========
tf_docs = {}

for doc in processed_docs:
    term_count = Counter(processed_docs[doc])
    tf_docs[doc] = {}

    for term in term_count:
        freq = term_count[term]
        tf = 1 + math.log(freq)
        tf_docs[doc][term] = tf

#print("\nTF:")
#for doc in tf_docs:
#    print(f"\n{doc}")
#   for term in tf_docs[doc]:
#        print(f"{term} : {tf_docs[doc][term]:.4f}")


# ======MENGHITUNG IDF (INVERSE DOCUMENT FREQUENCY)=======
idf = {}

total_docs = len(processed_docs)
all_terms = set()

for doc in processed_docs:
    for term in processed_docs[doc]:
        all_terms.add(term)

for term in all_terms:
    doc_count = 0
    for doc in processed_docs:
        if term in processed_docs[doc]:
            doc_count += 1

    idf[term] = math.log(total_docs / doc_count)

#print("\nIDF:")
#for term in idf:
#    print(f"{term} : {idf[term]:.4f}")


# =========MENGHITUNG TF-IDF DOKUMEN========
tfidf = {}

for doc in tf_docs:
    tfidf[doc] = {}
    for term in tf_docs[doc]:
        tfidf[doc][term] = tf_docs[doc][term] * idf[term]

#print("\nTF-IDF:")
#for doc in tfidf:
#    print(f"\n{doc}")
#    for term in tfidf[doc]:
#        print(f"{term} : {tfidf[doc][term]:.4f}")


# ========PREPROCESSING QUERY========
processed_query = preprocess(query)

print("\nProcessed Query:")
print(processed_query)


# ===========MENGHITUNG TF QUERY=========
query_tf = {}

term_count = Counter(processed_query)
for term in term_count:
    freq = term_count[term]
    query_tf[term] = 1 + math.log(freq)

print("\nQuery TF:")
print(query_tf)


# =====MENGHITUNG TF-IDF QUERY=====
query_tfidf = {}

for term in query_tf:
    if term in idf:
        query_tfidf[term] = query_tf[term] * idf[term]

print("\nQuery TF-IDF:")
print(query_tfidf)


# ======FUNGSI COSINE SIMILARITY======
def cosine_similarity(doc_vector, query_vector):

    dot_product = 0
    for term in query_vector:
        if term in doc_vector:
            dot_product += doc_vector[term] * query_vector[term]

    doc_norm = 0
    for value in doc_vector.values():
        doc_norm += value ** 2

    doc_norm = math.sqrt(doc_norm)
    query_norm = 0
    for value in query_vector.values():
        query_norm += value ** 2

    query_norm = math.sqrt(query_norm)
    if doc_norm == 0 or query_norm == 0:
        return 0

    return dot_product / (doc_norm * query_norm)


# =======MENGHITUNG COSINE SIMILARITY=========
similarities = {}

for doc in tfidf:
    sim = cosine_similarity(tfidf[doc], query_tfidf)
    similarities[doc] = sim

print("\nCosine Similarity:")

for doc in similarities:
    print(f"{doc} : {similarities[doc]:.4f}")


# ==========RANKING DOKUMEN==========
ranking = sorted(
    similarities.items(),
    key=lambda x: x[1],
    reverse=True
)

print("\nRanking Dokumen:")
rank = 1    
for doc, score in ranking:
    print(f"{rank}. {doc} -> {score:.4f}")
    rank += 1

#=======INDEX FILE=========
print("Index file telah dibuat")

with open("index.txt", "w") as f:
    for term in sorted(all_terms):
        line = term + ": "
        postings = []

        for doc in tfidf:
            if term in tfidf[doc]:
                weight = tfidf[doc][term]
                postings.append(f"{doc},{weight:.4f}")

        line += " ".join(postings)
        f.write(line + "\n")


#========WEIGHTS FILE==========
print("Weights file telah dibuat")

with open("weights.txt", "w") as f:
    for doc in tfidf:
        line = doc + ": "
        terms = []

        for term in tfidf[doc]:
            weight = tfidf[doc][term]
            terms.append(f"{term},{weight:.4f}")

        line += " ".join(terms)
        f.write(line + "\n")


#======RESPONSE FILE=========
print("Respone file telah dibuat")

with open("response.txt", "w") as f:
    valid_docs = []

    for doc, score in ranking:
        if score > 0.001:
            valid_docs.append((doc, score))

    f.write(str(len(valid_docs)) + "\n")
    for doc, score in valid_docs:
        f.write(f"{doc} {score:.4f}\n")