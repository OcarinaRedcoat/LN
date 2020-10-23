import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

import numpy as np
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn import svm
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn import metrics

class ClassifyModel:

    def __init__(self, model):
        self.model = model

    def printModel(self):
        print(self.model)

    def gen_features(self, train_file):
        label_set = set()   # non-repeated labels
        questions = []      # only questions
        allLabels = list()  # repeated labels: index allLabels[0] -> label of question_train[0]

        for line in train_file:
            label, question = line.split(' ', 1)

            if self.model == 'COARSE':
                coarse, fine = label.split(":",1)
                label_set.add(coarse)
                allLabels.append(coarse)
            else:
                label_set.add(label)
                allLabels.append(label)

            questions.append(question)

        return questions, allLabels, label_set


if (len(sys.argv) != 4):
    print('Error number of arguments.')
    exit(1)
if (sys.argv[1] == '-fine'):
    model = ClassifyModel('FINE')
elif (sys.argv[1] == '-coarse'):
    model = ClassifyModel('COARSE')
else:
    print('Error in sys.argv[1]: must be \"-fine\" or \"-coarse\".')
    exit(1)

# Open files with read permissions
train_file = open(sys.argv[2], 'r')
dev_file  = open(sys.argv[3], 'r')

questions, allLabels, label_set = model.gen_features(train_file)


# Transformar o set de todas as labels numa lista
label_lst = list(label_set)

# Stop words
stop_words = set(stopwords.words("english"))

questions_train_str = list()

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

for line in questions:
        # Tokenizer de cada questao e remocao de stopwords

        line = re.sub("`{2}.*'{2}", '', line)
        line = re.sub("[0-9^~`´'*+?\"]",'', line)

        token_line = word_tokenize(line)
        # Questions after tokenization

        quest2tokens = [w.lower() for w in token_line]


        stemmerTokens = [stemmer.stem(w) for w in quest2tokens]

        #lemmonTokens = [lemmatizer.lemmatize(w) for w in stemmerTokens]

        quest2str = ' '.join(stemmerTokens)
        #quest2str = ' '.join(lemmonTokens)

        # Adicionar a questao a uma lista de questoes

        questions_train_str.append(quest2str)


questions_dev = list()

for line in dev_file:
        # Tokenizer de cada questao e remocao de stopwords
        line = re.sub("`{2}.*'{2}", '', line)
        line = re.sub("[0-9^~`´'*+?]",'', line)

        token_line = word_tokenize(line)
        # Questions after tokenization

        quest2tokens = [w.lower() for w in token_line]


        stemmerTokens = [stemmer.stem(w) for w in quest2tokens]

        #lemmonTokens = [lemmatizer.lemmatize(w) for w in stemmerTokens]

        quest2str = ' '.join(stemmerTokens)
        #quest2str = ' '.join(lemmonTokens)

        # Adicionar a questao a uma lista de questoes

        questions_dev.append(quest2str)


countVectorizer = CountVectorizer()

train_raw_count = countVectorizer.fit_transform(questions_train_str)
test_raw_count  = countVectorizer.transform(questions_dev)



tfIdfTransformer = TfidfTransformer()
train_tfidf = tfIdfTransformer.fit_transform(train_raw_count)
test_tfidf  = tfIdfTransformer.transform(test_raw_count)

classifier = svm.SVC(kernel='linear')
classifier.fit(train_tfidf, allLabels)

labels_predict = classifier.predict(test_tfidf)

for prediction in labels_predict:
    print(prediction)

# Close files
train_file.close()
dev_file.close()
