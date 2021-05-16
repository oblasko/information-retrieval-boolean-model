import nltk
import re
nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import gutenberg
from nltk.corpus import stopwords
from nltk.stem import *

from linked_list import LinkedList

class InvertedIndex:
    def __init__(self):
        self.collection = []
        self.index = {}
        self.collection_ids = {}
        self.stop_words = set(stopwords.words('english'))
        self.download_collection()
        self.create_inverted_index()
        
    def download_collection(self):
        ps = PorterStemmer()
        reg = re.compile(r'[a-zA-Z]')
        c = 0
        for fileid in gutenberg.fileids():
            vocab = set(w.lower() for w in gutenberg.words(fileid))
            stemmed_vocab_list = []
            for word in vocab:
                if not reg.match(word):
                    continue
                word = ps.stem(word)
                if word in self.stop_words:
                    continue
                stemmed_vocab_list.append(word)

            stemmed_vocab = set(stemmed_vocab_list)
            self.collection.append((c, stemmed_vocab))
            self.collection_ids[c] = fileid
            c += 1
    
    def print_colection_stats(self):
        print("Number of documents: {}".format(len(self.collection)))
        total_words = 0
        for doc in self.collection[1]:
            total_words += len(doc)
        print("Number of words in the collection: {}".format(total_words))

    def print_document_stats(self):
        for fileid in gutenberg.fileids():
            num_chars = len(gutenberg.raw(fileid))
            num_words = len(gutenberg.words(fileid))
            num_sents = len(gutenberg.sents(fileid))
            num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
            print("="*30)
            print("Document - {}".format(fileid))
            print("Number of words in the document: {}".format(num_words))
            print("Number of sentences in the document: {}".format(num_sents))
            print("Average word length - {}".format(round(num_chars/num_words)))
            print("Average sentence length - {}".format(round(num_words/num_sents)))

    def create_inverted_index(self):
        #merge all vocabularies across the collection
        for doc_id, doc in self.collection:
            for word in doc:
                if word not in self.index:
                    self.index[word] = LinkedList()
                
                self.index[word].append(doc_id)
            

def test_inverted_index():
    In = InvertedIndex()
    #testing if the index contains any stopwords
    stop_words = set(stopwords.words('english'))
    for sw in stop_words:
        assert(sw not in In.index)
    for term, ids in In.index.items():
        print("term: {}, list: {}".format(term, ids.print()))

test_inverted_index()

#l = LinkedList()
#l.append(0)
#l.append(2)
#l.append(5)
#l.append(6)
#l.append(8)
#l.append(9)
#l.append(10)
#l.print()
