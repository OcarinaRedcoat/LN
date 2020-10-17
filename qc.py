import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

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

question_words = []

# Open files with read permissions
train_file = open(sys.argv[2], 'r')
dev_file  = open(sys.argv[3], 'r')

corpus = [line.lower() for line in train_file]

stop_words = set(stopwords.words("english"))

# Remove question specific words from the set of stopwords in nltk
stop_words.remove('what')
stop_words.remove('where')
stop_words.remove('when')
stop_words.remove('which')
stop_words.remove('who')
stop_words.remove('whom')
stop_words.remove('why')
# Remove other from spotwords list beacuse other is a fine label
stop_words.remove('other')

train_token =[]

for line in corpus:
        token_line = word_tokenize(line)
        token = [w for w in token_line if not w in stop_words]
        train_token.append(token)

print(train_token)


# Close files
train_file.close()
dev_file.close()