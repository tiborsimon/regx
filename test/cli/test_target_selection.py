#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    from unittest import mock

from regx.cli import parse_args


class NonRecursiveTargetSelection(TestCase):
    def test__no_target_specified__empty_args_list(self):
        args = []
        expected = None
        result = parse_args(args)
        result = result['t']
        self.assertEqual(expected, result)

    def test__target_can_be_added(self):
        args = ['-t', 'filename']
        expected = ['filename']
        result = parse_args(args)
        result = result['t']
        self.assertEqual(expected, result)

    def test__more_than_one_targets_can_be_added(self):
        args = ['-t', 'filename1', 'filename2']
        expected = ['filename1', 'filename2']
        result = parse_args(args)
        result = result['t']
        self.assertEqual(expected, result)

    def test__multiple_flags_can_be_used(self):
        args = ['-t', 'filename1', 'filename2', '-t', 'filename3']
        expected = ['filename1', 'filename2', 'filename3']
        result = parse_args(args)
        result = result['t']
        self.assertEqual(expected, result)


class RecursiveTargetSelection(TestCase):
    def test__no_target_specified__empty_args_list(self):
        args = []
        expected = None
        result = parse_args(args)
        result = result['tr']
        self.assertEqual(expected, result)

    def test__target_can_be_added(self):
        args = ['-tr', 'filename']
        expected = ['filename']
        result = parse_args(args)
        result = result['tr']
        self.assertEqual(expected, result)

    def test__more_than_one_targets_can_be_added(self):
        args = ['-tr', 'filename1', 'filename2']
        expected = ['filename1', 'filename2']
        result = parse_args(args)
        result = result['tr']
        self.assertEqual(expected, result)

    def test__multiple_flags_can_be_used(self):
        args = ['-tr', 'filename1', 'filename2', '-tr', 'filename3']
        expected = ['filename1', 'filename2', 'filename3']
        result = parse_args(args)
        result = result['tr']
        self.assertEqual(expected, result)


class RecursiveAndNonRecursive(TestCase):
    def test__mixed_arguments(self):
        args = ['-tr', 'filename1', 'filename2', '-t', 'filename3']
        expected_t = ['filename3']
        expected_tr = ['filename1', 'filename2']
        result = parse_args(args)
        result_t = result['t']
        result_tr = result['tr']
        self.assertEqual(expected_t, result_t)
        self.assertEqual(expected_tr, result_tr)


class ExcludeTargetSelection(TestCase):
    def test__no_exclude_pattern_specified__empty_args_list(self):
        args = []
        expected = None
        result = parse_args(args)
        result = result['e']
        self.assertEqual(expected, result)

    def test__exclude_pattern_can_be_added(self):
        args = ['-e', 'exclude pattern']
        expected = ['exclude pattern']
        result = parse_args(args)
        result = result['e']
        self.assertEqual(expected, result)

    def test__more_than_one_exclude_patterns_can_be_added(self):
        args = ['-e', 'exclude1', 'exclude2']
        expected = ['exclude1', 'exclude2']
        result = parse_args(args)
        result = result['e']
        self.assertEqual(expected, result)

    def test__multiple_flags_can_be_used(self):
        args = ['-e', 'exclude1', 'exclude2', '-e', 'exclude3']
        expected = ['exclude1', 'exclude2', 'exclude3']
        result = parse_args(args)
        result = result['e']
        self.assertEqual(expected, result)

