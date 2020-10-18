import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import numpy as np

class ClassifyModel:

    def __init__(self, model):
        self.model = model
    def printModel(self):
        print(self.model)

    def word_as_vectors(self):
        pass

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

label_set = set()
questions = []
allLabels = list()
for line in train_file:
    label, question = line.split(' ', 1)

    label_set.add(label)
    allLabels.append(label)

    questions.append(question)

'''
    A allLabels e uma lista de todas as labels mesmo repetidas, 
    ou seja o index allLabel[0] corresponde a label da question_train[0]

    label_set permite a que nao haja labels repetidas
'''

# Transformar o set de todas as labels numa lista
label_lst = list(label_set)

# Stop words, e adicionar, pontuacao as stopwords
stop_words = set(stopwords.words("english"))

stop_words.add('?')
stop_words.add(',')
stop_words.add(';')
stop_words.add('´')
stop_words.add('\'')
stop_words.add('!')

questions_train =[]
tokens = list()

for line in questions:
        # Tokenizer de cada questao e remocao de stopwords
        token_line = word_tokenize(line)
        token = [w for w in token_line if not w in stop_words]
        # Adicionar a questao a uma lista de questoes
        questions_train.append(token)

        # Adicionar o token a lista de tokens se ainda nao existir na lista
        for w in token:
            if w not in tokens:
                tokens.append(w)


word2vec = np.zeros((len(tokens), len(label_lst)))

for tindex in range(len(tokens)):
    for lindex in range(len(questions_train)):
        # saber qual a lablel da questao
        label_token = allLabels[lindex]

        if tokens[tindex] in questions_train[lindex]: #FIXME: se o token aparecer mais que uma vez
            # label_lst.index(label_token) index da label na lista de labels
            word2vec[tindex][label_lst.index(label_token)] += 1

print(word2vec)

# Close files
train_file.close()
dev_file.close()