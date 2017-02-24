#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on: Sep 21 2016

import pytest
import FMA_parse
from collections import OrderedDict
import os
import sys


def test_fma():
    out = FMA_parse.fma_parse('data.csv')
    with open('result.txt', 'r') as ifile:
        result = ifile.read()

    assert result == out


# this tests if there are multiple 'ultimate' parents
def test_many_parent():
    out = FMA_parse.fma_parse('many_parent_data.csv')
    with open('many_parent_result.txt', 'r') as ifile:
        result = ifile.read()

    assert result == out


# this is for an edge case -- testing if a file has only parents and no children
def test_only_parent():
    out = FMA_parse.fma_parse('only_parents_data.csv')
    with open('only_parents_result.txt', 'r') as ifile:
        result = ifile.read()

    assert result == out


# test for if parent is not in the data set --> orphaned_data list
def test_orphaned_data():
    out = FMA_parse.fma_parse('orphaned_data.csv')
    with open('orphaned_data_result.txt', 'r') as ifile:
        result = ifile.read()

    assert result == out


#def set_args():
#    my_args = ['FMA_parse', 'data.csv', 'result.txt']
#    print(my_args)
#    return my_args


def test_main(monkeypatch):
    monkeypatch.setattr(sys, "argv", ['FMA_parse', 'data.csv', 'result_monkey.txt'])
    print(sys.argv)
    # args = ['data.csv', 'result_main.txt']
    out = FMA_parse.main()
    with open('result.txt', 'r') as ifile:
        result = ifile.read()
    # remove file so that existing file error is not raised when re-running py.test --could also do a
    # naming scheme involving a time stamp on the result.txt name -- better to erase or have many files?
    os.remove('result_monkey.txt')

    assert result == out

#def test_main_file_exist():
#    args = ['data.csv', 'result_exist.txt']
#    with self.assertRaises(SystemExit) as cm:
#        FMA_parse.main(args)
#
#    the_exception = cm.exception
#    self.assertEqual(the_exception.code, 3)


def test_build():
    node = OrderedDict([('2', OrderedDict([('4', OrderedDict()), ('5', OrderedDict())])), ('3', OrderedDict())])
    output = "-1\n"
    level = 2
    out = FMA_parse.build(node, output, level)

    with open('result.txt', 'r') as ifile:
        result = ifile.read()
    assert result == out
