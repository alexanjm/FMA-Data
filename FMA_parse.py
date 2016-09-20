#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on: Sep 20 2016


def fma_parse(infile):

    infile = open(infile, 'r')
    parent_id_list = []
    tree = {}
    fma_loop_list = []
    parent_loop_list = []
    for line in infile:
        line = line.strip('\n')
        element_list = line.split(',')

        fma_id = element_list[0]
        parent_id = element_list[1]
        parent_id_list.append(element_list[1])

        if parent_id == '':
            tree[fma_id] = {}

        elif parent_id in parent_id_list:
            tree[parent_id][fma_id] = {}     # tree.setdefault(parent_id, {})

        else:
            fma_loop_list.append(fma_id)
            parent_loop_list.append(parent_id)
        print(fma_loop_list)
        print(parent_loop_list)
        print(parent_id)
        # print(tree)

    infile.close()


if __name__ == '__main__':
    fma_parse('/Users/jonesalm/Documents/playground/test_IDs.csv')
