"""Contains functions for input pipeline to the model"""
import numpy as np

def sort_txt(x):
    """:type x bytestring from camzip
    """

    text = x

    sequence = [char for char in text]

    return sequence


def generate_set(sequence, lookback):
    x, y = [], []
    # pad with first value in sequence so that first lookback values have context
    sequence = [sequence[0]]*lookback + sequence
    for i in range(len(sequence) - lookback):
        a = sequence[i:(i + lookback)]
        x.append(a)
        y.append(sequence[i + lookback])

    return np.array(x), np.array(y)


def context_freq(seq, k):

    freqs = {}

    new_seq = seq

    for i in range(len(new_seq)):

        if i < k:
            context = str(new_seq[:i])

        else:
            context = str(new_seq[i-k:i])

        if context not in freqs.keys():
            freqs[context] = {}

        if int(new_seq[i]) not in freqs[context].keys():
            freqs[context][int(new_seq[i])] = 0

        freqs[context][int(new_seq[i])] += 1

    return freqs





