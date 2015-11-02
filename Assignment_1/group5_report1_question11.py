"""Group5 Report1 Question11 builds a model of sequence times.

This module contains functions and a main that performs linear regression on
k-mer count features of sequences and sequencing time durations.

Five fold cross-validation is performed.

Example:
    Run with the path to a tsv containing sequences and labels and the kmer
    length as arguments.

        $python group5_report1_question11.py data/seq_times.tsv 3

kmers of length 3 were found to give the best performance.

The mean and variance of the R^2 values and across the 5 folds is provided.

The data points are shuffled to prevent any biases present in the order of the
data points.

Train set performance
        Mean R^2: 0.671546
        Var R^2: 0.001106

Test set performance
        Mean R^2: 0.649408
        Var R^2: 0.010450

"""

import sys
import numpy as np
from sklearn import linear_model

BASES = ['A', 'C', 'T', 'G']


def gen_kmers(k, prefix=""):
    """gen_kmers creates a lists of sequences with all kmers of lenght k
    with the given prefix

    This function recursively generates the kmers.

    Args:
        k: The length of the kmer variable region
        prefix: the prefix sequence, default is empty string.

    Returns:
        a list of sequences
    """
    if k == 0:
        return [prefix]
    to_return = []
    for base in BASES:
        new_prefix = prefix + base
        to_return.extend(gen_kmers(k - 1, new_prefix))
    return to_return


def k_mer_counts(seq, k, k_mer_dict):
    """k_mer_counts builds a feature vector of counts of all kmers

    Args:
        seq: the sequence to be featurized.
        k: The kmer length
        k_mer_dict: dictionary mapping k_mers to indices in feature vector.

    Returns:
        a feature vector so size 2<<(2*k)

    """
    # initialize feature vector with 0's
    feature_vector = [0] * (1 << (2 * k))

    # for each kmer component, increase the count in the feature vector
    for i in range(0, len(seq) - k):
        k_mer = seq[i:i + k]
        feature_vector[k_mer_dict[k_mer]] += 1
    return feature_vector


def shuffle_feature_vectors_and_labels(X, Y):
    """shuffle_feature_vectors_and_labels randomizes the order of the
    feature vectors and labels.

    Args:
        X: feature vectors
        Y: labels

    Returns:
        randomized feature vectors and labels
    """

    perms = np.random.permutation(len(X))
    X_p = []
    Y_p = []
    for i in range(0, len(X)):
        X_p.append(X[perms[i]])
        Y_p.append(Y[perms[i]])
    return X_p, Y_p


def main(argv):
    # Check valid inputs given.
    if len(argv) != 3:
        sys.stderr.write("invalid usage: python group5_report1_question11.py" +
                         " <data_labels.tsv> <k_mer_size>\n")
        sys.exit(2)

    data_labels_fn = argv[1]

    k = int(argv[2])
    k_mers = gen_kmers(k)

    k_mer_dict = {}
    for i, k_mer in enumerate(k_mers):
        k_mer_dict[k_mer] = i

    # load genes info from json into a dictionary
        # Presumably this file will be small enough that doing this is not a
        # problem.
    data_labels = open(data_labels_fn)

    X = []
    Y = []
    first = True  # we want to skip the first line, whcih is headings.
    print "loading in data"
    for l in data_labels:
        # skip the first line.
        if first:
            first = False
            continue

        [seq, label] = l.split()
        feature_vector = k_mer_counts(seq, k, k_mer_dict)
        label_val = int(label)
        X.append(feature_vector)
        Y.append(label_val)

    print "loaded %d sequences" % len(X)

    # shuffle data
    X, Y = shuffle_feature_vectors_and_labels(X, Y)

    # train test split
    num_folds = 5
    fold_size = len(X) / num_folds
    folds = []

    for split in range(5):
        X_train = X[:split * fold_size] + X[(split + 1) * fold_size:]
        Y_train = Y[:split * fold_size] + Y[(split + 1) * fold_size:]
        X_test = X[split * fold_size:(split + 1) * fold_size]
        Y_test = Y[split * fold_size:(split + 1) * fold_size]
        train = (X_train, Y_train)
        test = (X_test, Y_test)
        folds.append((train, test))

    print "len train: %d" % len(X_train)
    print "len test: %d" % len(X_test)

    # initialize sklearn regression model.
    regr = linear_model.LinearRegression()

    print "performing cross validation on %d folds" % num_folds
    training_R_sqr = []
    testing_R_sqr = []
    for i, ((X_train, Y_train), (X_test, Y_test)) in enumerate(folds):
        print "fitting fold %d/%d" % (i + 1, num_folds)
        regr.fit(X_train, Y_train)

        # Explained variance score: 1 is perfect prediction
        R_sqr_train = regr.score(X_train, Y_train)
        training_R_sqr.append(R_sqr_train)

        # Explained variance score: 1 is perfect prediction
        R_sqr_test = regr.score(X_test, Y_test)
        testing_R_sqr.append(R_sqr_test)

    print "Train set performance"
    print "\tMean R^2: %f" % np.mean(training_R_sqr)
    print "\tVar R^2: %f" % np.var(training_R_sqr)

    print "\nTest set performance"
    print "\tMean R^2: %f" % np.mean(testing_R_sqr)
    print "\tVar R^2: %f" % np.var(testing_R_sqr)


if __name__ == "__main__":
    main(sys.argv)
