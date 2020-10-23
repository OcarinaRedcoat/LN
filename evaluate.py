import sys
from sklearn import metrics

model  = sys.argv[1]
y_test = open(sys.argv[2])
y_pred = open(sys.argv[3])

y_label = list()
y_res = list()

for line in y_pred:
    aux, trash = line.split('\n')
    y_res.append(aux)


for line in y_test:

    if sys.argv[1] == '-coarse':
        coarse, fine = line.split(":",1)
        y_label.append(coarse)
    else:
        aux, trash = line.split('\n')
        y_label.append(aux)


# Model Accuracy: how often is the classifier correct?
#print(y_res)
#print('-')
#print(y_label)
print("Accuracy:",metrics.accuracy_score(y_res, y_label))
