#!/usr/bin/env python
"""
Splits input data into train, dev, and test sets. Optional verbose mode.

This script will take an input dataset and split it into the following proportions:
80% training, 10% development, 10% testing.

There is an optional -v that enables verbose mode, which will share the number
of sentences and tokens in each output file.

# noqa: E501
"""

import argparse
import random
import logging

from typing import Iterator, List


# reads data by sentence
def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
    # Just in case someone forgets to put a blank line at the end...
    if lines:
        yield lines


def write_tags(path: str, corpus: list) -> None:
    with open(path, "w") as sink:
        sentence_counter = 0
        token_counter = 0
        for sentence in corpus:
            counter = 0
            for word in sentence:
                print(
                    " ".join(word)
                    if counter != len(sentence) - 1
                    else " ".join(word) + "\n",
                    file=sink,
                )
                token_counter += 1
                counter += 1
            sentence_counter += 1
        logging.info(
            f"{path} contains {token_counter} tokens"
            + "across {sentence_counter} sentences."
        )


def main(args: argparse.Namespace) -> None:
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    corpus = list(read_tags(args.input))
    random.seed(args.seed)
    random.shuffle(corpus)
    length = len(corpus)
    eighty = int(0.8 * length)
    ninety = int(0.9 * length)
    train = corpus[0:eighty]
    dev = corpus[eighty:ninety]
    test = corpus[ninety:length]
    write_tags(args.train, train)
    write_tags(args.dev, dev)
    write_tags(args.test, test)


if __name__ == "__main__":
    # TODO: declare arguments.
    # TODO: parse arguments and pass them to `main`.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True, help="seed for PRNG")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        help="enables verbose mode",
    )
    parser.add_argument("input", help="input initial data file")
    parser.add_argument("train", help="output training data file")
    parser.add_argument("dev", help="output development data file")
    parser.add_argument("test", help="output testing data file")
    main(parser.parse_args())
