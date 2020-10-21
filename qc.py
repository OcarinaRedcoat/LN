import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import numpy as np

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

from sklearn import svm
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn import metrics

class ClassifyModel:

    def __init__(self, model):
        self.model = model
    def printModel(self):
        print(self.model)

    def word_as_vectors(self):
        pass
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


'''
label_set = set()   # non-repeated labels
questions = []      # only questions
allLabels = list()  # repeated labels: index allLabels[0] -> label of question_train[0]
'''

questions, allLabels, label_set = model.gen_features(train_file)


# Transformar o set de todas as labels numa lista
label_lst = list(label_set)

# Stop words
stop_words = set(stopwords.words("english"))
# adicionar pontuacao as stopwords
stop_words.add('?')
stop_words.add(',')
stop_words.add(';')
stop_words.add('´')
stop_words.add('\'')
stop_words.add('!')
stop_words.add('.')
stop_words.add('\'s')


questions_train = []
questions_train_str = list()
tokens = list()     # list of tokens

for line in questions:
        # Tokenizer de cada questao e remocao de stopwords
        token_line = word_tokenize(line)
        # Questions after tokenization
        quest2tokens = [w for w in token_line if not w in stop_words]

        quest2str = ' '.join(quest2tokens)

        # Adicionar a questao a uma lista de questoes
        questions_train.append(quest2tokens)
        questions_train_str.append(quest2str)

        # Adicionar o token a lista de tokens se ainda nao existir na lista
        for w in quest2tokens:
            if w not in tokens:
                tokens.append(w)


def preprocessDev(devFile):
    questions_dev = list()
    for line in devFile:
        token_line = word_tokenize(line)
        quest2tokens = [w for w in token_line if not w in stop_words]
        quest2str = ' '.join(quest2tokens)
        questions_dev.append(quest2str)
    return questions_dev

questions_dev = preprocessDev(dev_file)


word2vec = np.zeros((len(tokens), len(label_lst)))

# Atencao que so funcionar para --coarse devido as labels
for tindex in range(len(tokens)):
    for lindex in range(len(questions_train)):
        # saber qual a lablel da questao
        label_token = allLabels[lindex]

        if tokens[tindex] in questions_train[lindex]:
            # label_lst.index(label_token) index da label na lista de labels
            how_many_tokens = questions_train[lindex].count(tokens[tindex])
            word2vec[tindex][label_lst.index(label_token)] += how_many_tokens

'''
trainCountVectorize = CountVectorizer()
wordCount = trainCountVectorize.fit_transform(questions_train_str)

#print(word2vec)
trainTfIdfTransformer = TfidfTransformer()
TfIdf = trainTfIdfTransformer.fit_transform(wordCount)
print(wordCount.shape)
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(TfIdf, allLabels)

devCountVectorize = CountVectorizer()
devTfIdfTransformer = TfidfTransformer()

countDec =  devCountVectorize.fit_transform(questions_dev)
devTfIdf = devTfIdfTransformer.fit_transform(countDec)
print(countDec.shape)
#sys.exit(0)
#Predict the response for test dataset
y_pred = clf.predict(devTfIdf)

print(y_pred)
'''

countVectorizer = CountVectorizer(binary=True)

train_raw_count = countVectorizer.fit_transform(questions_train_str)
test_raw_count  = countVectorizer.transform(questions_dev)



tfIdfTransformer = TfidfTransformer(use_idf=True)
train_tfidf = tfIdfTransformer.fit_transform(train_raw_count)
test_tfidf  = tfIdfTransformer.transform(test_raw_count)

classifier = svm.SVC(kernel='linear')
classifier.fit(train_raw_count, allLabels)

labels_predict = classifier.predict(test_tfidf)#.reshape(train_tfidf.shape)
result = list()
for i in labels_predict:
    result.append(i)

print(result)

y_test = open('DEV-labels.txt', 'r')
y_label = list()
for line in y_test:

    if sys.argv[1] == '-coarse':
        coarse, fine = line.split(":",1)
        y_label.append(coarse)
    else:
        aux, trash = line.split('\n')
        y_label.append(aux)
print(y_label)
#y_res = y_pred.readlines()
#print(y_res[0])
#print(y_label)

# Model Accuracy: how often is the classifier correct?

print("Accuracy:",metrics.accuracy_score(y_label, result))

# Close files
train_file.close()
dev_file.close()
