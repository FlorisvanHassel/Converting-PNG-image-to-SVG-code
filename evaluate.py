from __future__ import division
import numpy as np
import sys
import zipfile
import logging

def CER(predictions, references):
    """Given a list of predicted strings and a list of reference strings, 
    return the mean Character Error Rate.
    The Character Error Rate is the Levenshtein distance between the two strings
    divided by the length of the reference string."""
    return np.mean([ ed(p, r) / len(r) for p, r in zip(predictions, references)])

def ed(seq1, seq2):
    """Return the Levenshtein edit distance between seq1 and seq2."""
    oneago = None
    thisrow = list(range(1, len(seq2) + 1)) + [0]
    for x in range(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in range(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    d = thisrow[len(seq2) - 1]
    return d

    
def load(path, zipped=True):
    js = range(48000, 50000)
    strings = []
    if zipped:
        with zipfile.ZipFile(path) as z:
            for j in js:
                strings.append(z.open("{}.svg".format(j)).read())
    else:
        for j in js:
                strings.append(open("{}/{}.svg".format(path, j)).read())
                
    return strings

    
def main():
    logging.basicConfig(level=logging.INFO)
    indir = sys.argv[1]
    outdir = sys.argv[2]

    solution = load(indir+ "/ref/svg", zipped=True)
    logging.info("Loading solution")
    submitted = load(indir+ "/res/", zipped=False)
    logging.info("Loading reference")
    with open(outdir + "/scores.txt", 'w') as f:
        result = CER(submitted, solution)
        logging.info("Result was {}".format(result))
        f.write("CER: {}\n".format(result))

if __name__ == '__main__':
    main()

