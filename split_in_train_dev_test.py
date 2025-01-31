#!/usr/bin/env python
"""

Neural SPARQL Machines - Split into train, dev, and test sets.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://arxiv.org/abs/1708.07624

Version 1.0.0

"""
import argparse
import io
import os
import random

TRAINING_PERCENTAGE = 80
TEST_PERCENTAGE = 10
DEV_PERCENTAGE = 10

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--lines', dest='lines', metavar='lines',
                               help='total number of lines (wc -l <file>)', required=True)
    requiredNamed.add_argument('--dataset', dest='dataset',
                               metavar='dataset.sparql', help='sparql dataset file', required=True)
    args = parser.parse_args()

    lines = int(args.lines)
    dataset_file = os.path.splitext(args.dataset)[0]
    sparql_file = dataset_file + '.sparql'
    en_file = dataset_file + '.en'

    random.seed()

    test_and_dev_percentage = sum([TEST_PERCENTAGE, DEV_PERCENTAGE])
    number_of_test_and_dev_examples = int(
        lines * test_and_dev_percentage / 100)
    number_of_dev_examples = int(
        number_of_test_and_dev_examples * DEV_PERCENTAGE / test_and_dev_percentage)

    dev_and_test = random.sample(range(lines), number_of_test_and_dev_examples)
    dev = random.sample(dev_and_test, number_of_dev_examples)
    with io.open(sparql_file, encoding="utf-8") as original_sparql, io.open(en_file, encoding="utf-8") as original_en:
        sparql = original_sparql.readlines()
        english = original_en.readlines()

        dev_sparql_lines = []
        dev_en_lines = []
        train_sparql_lines = []
        train_en_lines = []
        test_sparql_lines = []
        test_en_lines = []

        for i in range(len(sparql)):
            sparql_line = sparql[i]
            en_line = english[i]
            if i in dev_and_test:
                if i in dev:
                    dev_sparql_lines.append(sparql_line)
                    dev_en_lines.append(en_line)
                else:
                    test_sparql_lines.append(sparql_line)
                    test_en_lines.append(en_line)
            else:
                train_sparql_lines.append(sparql_line)
                train_en_lines.append(en_line)

        with io.open('train.sparql', 'w', encoding="utf-8") as train_sparql, io.open('train.en', 'w', encoding="utf-8") as train_en, \
                io.open('dev.sparql', 'w', encoding="utf-8") as dev_sparql, io.open('dev.en', 'w', encoding="utf-8") as dev_en, \
                io.open('test.sparql', 'w', encoding="utf-8") as test_sparql, io.open('test.en', 'w', encoding="utf-8") as test_en:

            train_sparql.writelines(train_sparql_lines)
            train_en.writelines(train_en_lines)
            dev_sparql.writelines(dev_sparql_lines)
            dev_en.writelines(dev_en_lines)
            test_sparql.writelines(test_sparql_lines)
            test_en.writelines(test_en_lines)
