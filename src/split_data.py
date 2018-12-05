import argparse
import os
import csv
import math

def count_lines(corpus_file):
    """ left over only line wise
    Source: https://stackoverflow.com/a/9631635 """
    def blocks(files, size=65536):
        while True:
            b = files.read(size)
            if not b: break
            yield b
    print("Counting lines..")
    with open(corpus_file, 'r', encoding="utf8", errors='ignore') as f_in:
        n_lines = sum(bl.count("\n") for bl in blocks(f_in))
    return n_lines

def count_entries(corpus_file):
    print("Counting lines..")
    with open(corpus_file, 'r', encoding='utf-8', errors='ignore') as f_in:
        f_csv = csv.DictReader(f_in)
        n_lines = sum(1 for _ in f_csv)
    return n_lines

def main(args):
    if ((args.train + args.test + args.val) > 1):
        print("Split percentages sum to > 1, check.")
        sys.exit(1)
    line_count = count_entries(args.f)
    train_index = line_count * args.train
    test_index = train_index + line_count * args.test
    val_index = test_index + line_count * args.val
    data = []
    print("Splitting %s sentences, (%s train, %s test, %s validation).." %
            (line_count,
            math.floor(train_index),
            math.floor(test_index-train_index),
            math.floor(val_index-test_index)))
    out = os.path.splitext(os.path.abspath(args.out))[0]
    with open(args.f, encoding = 'utf-8', mode = 'r') as corpus:
        csv_corpus = csv.DictReader(corpus)
        fieldnames = csv_corpus.fieldnames
        # Reading in data
        if args.pbar:
            from tqdm import tqdm
            iterator = tqdm(enumerate(csv_corpus), total = line_count)
            # iterator = tqdm(enumerate(corpus), total = line_count)
        else:
            iterator = enumerate(csv_corpus)
        # standard out files
        with open("%s-train.csv" % out, encoding = 'utf-8', mode = 'w') as train_f:
            train_out = csv.DictWriter(train_f, fieldnames = fieldnames)
            with open("%s-test.csv" % out, encoding = 'utf-8', mode = 'w') as test_f:
                test_out = csv.DictWriter(test_f, fieldnames = fieldnames)
                for index, line in iterator:
                    if index <= train_index:
                        train_out.writerow(line)
                    elif index <= test_index:
                        test_out.writerow(line)
                    else:
                        break;
        if args.val > 0.0: # in case we want validation data
            with open("%s-validation.csv" % out, 'w', encoding = 'utf-8') as val_f:
                val_out = csv.DictWriter(val_f, fieldnames = fieldnames)
                for index, line in iterator:
                    val_out.writerow(line)

if(__name__ == "__main__"):
    # TODO: kuerzel fuer die opts? Also -o bzw --outputFile
    parser = argparse.ArgumentParser(description='Params')
    parser.add_argument('--f', required=True,type = str,
                        help='TODO')
    parser.add_argument('--pbar', action='store_true',
                        help = 'Will output a progress bar,' \
                        + "requires tqdm!")
    parser.add_argument('--out', type = str, required = True,
                        help = 'Path where to write the resulting corpora.')
    parser.add_argument('--train', type = float, default = 0.8,
                        help = 'Amount of train data')
    parser.add_argument('--test', type = float, default = 0.2,
                        help = 'Amount of test data')
    parser.add_argument('--val', type = float, default = 0.0,
                        help = 'Amount of validation data')
    args = parser.parse_args()
    main(args)
