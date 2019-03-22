from trees import *
from vl_codes import *
import arithmetic
import numpy as np
from itertools import groupby
from json import dump
from sys import argv
from adaptive import txtin, train1


def camzip(method, filename, cont_length=None):

    with open(filename, 'rb') as fin:
        x = fin.read()

    if method == 'context':
        seq = txtin.sort_txt(x)
        frequencies = txtin.context_freq(seq, cont_length)
        n = dict([(a, sum(frequencies[a].values())) for a in frequencies])

        p = frequencies.copy()

        for context in p:
            p[context] = dict([(a, p[context][a]/n[context]) for a in p[context]])

    else:
        frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(x))])
        n = sum([frequencies[a] for a in frequencies])
        p = dict([(a, frequencies[a]/n) for a in frequencies])

    if method == 'huffman' or method == 'shannon_fano':
        if (method == 'huffman'):
            xt = huffman(p)
            print(xtree2newick(xt)) #Added
            c = xtree2code(xt)
        else:
            c = shannon_fano(p)
            xt = code2xtree(c)
            print(c)  # Added

        y = vl_encode(x, c)

    elif method == 'arithmetic':
        y = arithmetic.encode(x,p)

    elif method == 'context':
        y = arithmetic.encode_c(seq, p, cont_length)

    else:
        raise NameError('Compression method %s unknown' % method)

    y = bytes(bits2bytes(y))

    
    outfile = filename + '.cz' + method[0]

    with open(outfile, 'wb') as fout:
        fout.write(y)

    pfile = filename + '.czp' + method[0]
    n = len(x)

    with open(pfile, 'w') as fp:
        dump(frequencies, fp)


def camzip_cont(filename):
    """Camzip function for use with the model method"""

    with open(filename, 'rb') as fin:
        xfull = fin.read()

    seq = txtin.sort_txt(xfull)

    #seq = [32 if x==9 else x for x in seq]

    print(len(seq))

    xset, yset = txtin.generate_set(seq, 3)

    xset = np.reshape(xset, (xset.shape[0], 1, xset.shape[1]))

    #print(train1.train_model(xset, yset))

    dists = np.float64(train1.load_dist(xset, 'model5.h5'))

    print(dists[0])  # the first distribution is for the 6th symbol in hamlet.txt
    # Going to pad the start of hamlet with 5 of the first symbol
    # predict for one value then encode then the next etc
    # use the same model should give the same code words
    # predict one value, encode, predict next, etc etc
    # same with decoder if all previous symbols decoded properly
    # can either save the model and random seed or save the distributions
    # having the model and seed would mean that no communication is required between the encoding and decoding
    # the model is also specific to hamlet.txt of course
    # machines for any text. Saving the distributions requires this communication and is specific to hamlet.txt
    # could extend to full works of shakespeare for example

    dist_list = []

    for i in range(len(dists)):
        dist = dists[i]
        new_dict = dict([(a, dist[a]) for a in range(len(dist))])
        dist_list.append(new_dict)

    y = arithmetic.encode_cont(xfull, dist_list)

    y = bytes(bits2bytes(y))

    outfile = filename + '.czm'

    with open(outfile, 'wb') as fout:
        fout.write(y)

    pfile = filename + '.czpm'

    new_dist_list = []
    for i in range(len(dist_list)):
        new_dist_list.append({dist_list[i][a].item() for a in dist_list[i]})

    with open(pfile, 'w') as fp:
        dump(dist_list, fp)


if __name__ == "__main__":
    if (len(argv) != 3):
        print('Usage: python %s compression_method filename\n' % argv[0])
        print('Example: python %s huffman hamlet.txt' % argv[0])
        print('or:      python %s shannon_fano hamlet.txt' % argv[0])
        print('or:      python %s arithmetic hamlet.txt' % argv[0])
        exit()

    camzip(argv[1], argv[2])


