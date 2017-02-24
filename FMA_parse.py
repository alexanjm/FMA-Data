#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on: Sep 20 2016
import argparse
from collections import OrderedDict
import re
import sys
import os
from buddysuite import buddy_resources as br


def build(node, output, level):
    print("Node is:", node)
    print("output is:", output)
    print("Level is", level)
    for fmaid, subnode in node.items():
        output += "%s%s\n" % ("-" * level, fmaid)
        if node[fmaid]:
            output = build(node[fmaid], output, level + 1)
    print("final output is:", output)
    return output


def fma_parse(infile):
    # Start by parsing the input file into an OrderedDict
    with open(infile, 'r') as ifile:
        data = ifile.read().strip()
        data = re.sub("\|.*,", ",", data)
        data = data.split("\n")
        data = OrderedDict([tuple(x.strip().split(",")) for x in data[1:]])
    orphaned_data = []  # This should remain empty if the input data is correct
    connected_data = []
    for fmaid, parent in data.items():
        node = [fmaid]
        valve = br.SafetyValve()
        while True:
            valve.step()
            if parent == "":
                node.reverse()
                connected_data.append(node)
                break
            elif parent not in data:
                node.append(parent)
                node.reverse()
                orphaned_data.append(node)
                break
            else:
                node.append(parent)
                parent = data[parent]

    # Build up an hierarchical dictionary, appending new dicts for each new node encountered
    tree = OrderedDict()
    for ancestry in connected_data:
        tree.setdefault(ancestry[0], OrderedDict())
        node = tree[ancestry[0]]
        for fmaid in ancestry[1:]:
            node.setdefault(fmaid, OrderedDict())
            node = node[fmaid]

    # Recursively traverse the hierarchical dictionary to build the output string
    output = ""
    # print(tree)
    for fmaid, node in tree.items():
        output += "-%s\n" % fmaid
        # print(node)
        print("output into build", output)
        print("node into build is:", node)
        output = build(node, output, 2)
    if orphaned_data:  # This will only happen if the input data is incorrect
        print("WARNING! The CSV file provided contains 'orphaned' branches which do not link back to the parentless"
              " top nodes. You'll need to modify the source code to see what's-the-what.")
        # Uncomment the following to print the orphaned nodes
        # print(orphaned_data)

    return output


def main():
    parser = argparse.ArgumentParser(prog="FMA_parse", description="Convert FMA csv to hierarchical dictionary")
    parser.add_argument('csv_file', help='Where is the FMA csv file? Note'
                                         ' that this file MUST contain a header line.',
                        action='store')
    parser.add_argument('output', help="Where should we save the tree?", action='store')

    in_args = parser.parse_args()

    if os.path.isfile(in_args.output):
        print("Output file already exists. I'm quiting so you don't accidentally overwrite data.")
        sys.exit()

    results = fma_parse(in_args.csv_file)
    print("results is:", results)
    with open(in_args.output, "w") as ofile:
        ofile.write(results)

    return results


if __name__ == '__main__':
    print("hello")
    main_output = main()

    # return main_output
