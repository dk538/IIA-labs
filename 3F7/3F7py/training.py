import numpy as np
from adaptive import txtin, train1

filenames = ['coriolanus.txt', 'titus.txt', 'romeoandjuliet.txt', 'othello.txt', 'julius.txt', 'troilus.txt']

seq = []

for filename in filenames:
    with open(filename, 'rb') as fin:
        xfull = fin.read()
        seq.extend(txtin.sort_txt(xfull))

print(len(seq))

xset, yset = txtin.generate_set(seq, 3)

xset = np.reshape(xset, (xset.shape[0], 1, xset.shape[1]))

train1.set_seed()

print(train1.train_model(xset, yset))