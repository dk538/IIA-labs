from trees import *
from vl_codes import *
import arithmetic
from json import load
from sys import argv, exit


def camunzip(filename, cont_length=None):
    if filename[-1] == 'h':
        method = 'huffman'
    elif filename[-1] == 's':
        method = 'shannon_fano'
    elif filename[-1] == 'a':
        method = 'arithmetic'
    elif filename[-1] == 'c':
        method = 'context'
    else:
        raise NameError('Unknown compression method')
    
    with open(filename, 'rb') as fin:
        y = fin.read()
    y = bytes2bits(y)

    pfile = filename[:-1] + 'p' + method[0]

    with open(pfile, 'r') as fp:
        frequencies = load(fp)

    if method == 'context':

        n = dict([(a, sum(frequencies[a].values())) for a in frequencies])

        length = sum(n.values())

        p = frequencies.copy()

        for context in p:
            p[context] = dict([(a, p[context][a] / n[context]) for a in p[context]])

    else:

        n = sum([frequencies[a] for a in frequencies])
        print(n)
        p = dict([(int(a),frequencies[a]/n) for a in frequencies])

    if method == 'huffman' or method == 'shannon_fano':
        if (method == 'huffman'):
            xt = huffman(p)
            c = xtree2code(xt)
        else:
            c = shannon_fano(p)
            xt = code2xtree(c)

        x = vl_decode(y, xt)

    elif method == 'arithmetic':
        x = arithmetic.decode(y,p,n)

    elif method == 'context':
        x = arithmetic.decode_c(y, p, length, cont_length)

    else:
        raise NameError('This will never happen (famous last words)')
    
    # '.cuz' for Cam UnZipped (don't want to overwrite the original file...)
    outfile = filename[:-4] + '.cuz' 

    with open(outfile, 'wb') as fout:
        fout.write(bytes(x))

def camunzip_cont(filename):
    """Camzip function for use with the model method"""

    with open(filename, 'rb') as fin:
        y = fin.read()
    y = bytes2bits(y)

    pfile = filename[:-1] + 'pm'
    with open(pfile, 'r') as fp:
        dists = load(fp)
    n = len(dists)

    x = arithmetic.decode_cont(y, dists)

    outfile = filename[:-5] + '.cuz'

    with open(outfile, 'wb') as fout:
        fout.write(bytes(x))


if __name__ == "__main__":
    if (len(argv) != 2):
        print('Usage: python %s filename\n' % argv[0])
        print('Example: python %s hamlet.txt.czh' % argv[0])
        print('or:      python %s hamlet.txt.czs' % argv[0])
        print('or:      python %s hamlet.txt.cza' % argv[0])
        exit()

    camunzip(argv[1])
