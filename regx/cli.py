#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


def _merge_args(args):
    for key in args:
        if args[key]:
            temp = args[key]
            args[key] = []
            for item in temp:
                args[key].extend(item)
    return args


def parse_args(raw_args):
    parser = argparse.ArgumentParser(description='Argument parser experiment')

    # targets
    parser.add_argument('-t', action='append', nargs='+')
    parser.add_argument('-tr', action='append', nargs='+')
    parser.add_argument('-e', action='append', nargs='+')

    args = vars(parser.parse_args(raw_args))

    return _merge_args(args)
