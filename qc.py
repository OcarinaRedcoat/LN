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

'''
        coarse = []
        fine = []
        if self.model == 'COARSE':
            coarse, fine = labels.split(':',1)
            return coarse
        else:
            return labels
'''
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


questions_train = [] 
tokens = list()     # list of tokens

for line in questions:
        # Tokenizer de cada questao e remocao de stopwords
        token_line = word_tokenize(line)
        # Questions after tokenization
        quest2tokens = [w for w in token_line if not w in stop_words]
        # Adicionar a questao a uma lista de questoes
        questions_train.append(quest2tokens)

        # Adicionar o token a lista de tokens se ainda nao existir na lista
        for w in quest2tokens:
            if w not in tokens:
                tokens.append(w)


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

print(word2vec)

# Close files
train_file.close()
dev_file.close()