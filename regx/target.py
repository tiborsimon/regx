#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


def _generate_level_struct(path, depth):
    files = {}
    for r, d, f in os.walk(path):
        common_path = os.path.commonprefix([path, r])
        common = len(common_path.split(os.sep))
        level = len(r.split(os.sep))-common
        if level not in files:
            files[level] = []
        for file in f:
            files[level].append(os.path.join(r, file))
    return files

def _select_all_levels(files):
    ret = []
    for level in files:
        ret.extend(files[level])
    return ret


def _select_files_for_depth(files, depth, exclusive):
    ret = []
    if exclusive:
        ret = files[depth]
    else:
        if depth == 0:
            ret.extend(files[0])
        else:
            for i in range(depth+1):
                if i in files:
                    ret.extend(files[i])
    return ret


def _get_files_from_dir(path, depth=-1, exclusive=False):
    files = _generate_level_struct(path, depth)
    if depth == -1:
        return _select_all_levels(files)
    else:
        return _select_files_for_depth(files, depth, exclusive)


def _check_exclude(f, exclude_patterns):
    for p in exclude_patterns:
        if re.search(p, f):
            return False
    return True


def load(args):
    ret = []
    for name in args['t']:
        path = os.path.relpath(name, '.')
        if os.path.isdir(path):
            ret = _get_files_from_dir(path, depth=0, exclusive=True)
        elif os.path.isfile(path):
            ret.append(path)
    for name in args['tr']:
        path = os.path.relpath(name, '.')
        if os.path.isdir(path):
            ret = _get_files_from_dir(path, depth=-1, exclusive=False)
        elif os.path.isfile(path):
            ret.append(path)
    for depth, name in args['trd']:
        path = os.path.relpath(name, '.')
        if os.path.isdir(path):
            ret = _get_files_from_dir(path, depth=depth, exclusive=False)
        elif os.path.isfile(path):
            ret.append(path)
    for depth, name in args['trdo']:
        path = os.path.relpath(name, '.')
        if os.path.isdir(path):
            ret = _get_files_from_dir(path, depth=depth, exclusive=True)
        elif os.path.isfile(path):
            ret.append(path)
    if args['e']:
        ret = [f for f in ret if _check_exclude(f, args['e'])]
    return ret

