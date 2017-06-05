#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

from regx import target


class FileLoadingFromDir(TestCase):
    @mock.patch.object(target.os, 'walk')
    def test__files_can_be_loaded_from_dir_root(self, mock_walk):
        path = '.'
        depth = 1
        expected = ['./file1', './file2']
        mock_walk.return_value = [
            ('.', [], ['file1', 'file2'])
        ]
        ret = target._get_files_from_dir(path, depth)
        self.assertEqual(expected, ret)

    @mock.patch.object(target.os, 'walk')
    def test__depth_can_be_controlled(self, mock_walk):
        path = '.'
        depth = 0
        expected = ['./file1']
        mock_walk.return_value = [
            ('.', [], ['file1']),
            ('./d1', [], ['file2'])
        ]
        ret = target._get_files_from_dir(path, depth)
        self.assertEqual(expected, ret)

    @mock.patch.object(target.os, 'walk')
    def test__file_returned_from_depth_1(self, mock_walk):
        path = '.'
        depth = 1
        expected = ['./d1/file2']
        mock_walk.return_value = [
            ('.', [], []),
            ('./d1', [], ['file2'])
        ]
        ret = target._get_files_from_dir(path, depth)
        self.assertEqual(expected, ret)

    @mock.patch.object(target.os, 'walk')
    def test__greater_depth_with_non_exclusive_mode_is_fine(self, mock_walk):
        path = '.'
        depth = 9
        expected = ['./file1', './d1/file2']
        mock_walk.return_value = [
            ('.', [], ['file1']),
            ('./d1', [], ['file2'])
        ]
        ret = target._get_files_from_dir(path, depth)
        self.assertEqual(expected, ret)

    @mock.patch.object(target.os, 'walk')
    def test__exclusive_depth(self, mock_walk):
        path = '.'
        depth = 1
        exclusive = True
        expected = ['./d1/file2']
        mock_walk.return_value = [
            ('.', [], ['file1']),
            ('./d1', [], ['file2'])
        ]
        ret = target._get_files_from_dir(path, depth, exclusive)
        self.assertEqual(expected, ret)

    @mock.patch.object(target.os, 'walk')
    def test__greater_depth_with_exclusive_mode__raises_error(self, mock_walk):
        path = '.'
        depth = 9
        exclusive = True
        expected = ['./file1', './d1/file2']
        mock_walk.return_value = [
            ('.', [], ['file1']),
            ('./d1', [], ['file2'])
        ]
        with self.assertRaises(Exception) as ec:
            target._get_files_from_dir(path, depth, exclusive)
        self.assertEqual(ec.exception.__class__, KeyError)


class Flag_t(TestCase):
    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    def test__flag_t__single_file(self, mock_relpath, mock_isfile):
        args = {
            't':    ['file'],
            'tr':   [],
            'trd':  [],
            'trdo': [],
            'e':    []
        }
        mock_relpath.return_value = './file'
        mock_isfile.return_value = True
        expected = ['./file']
        result = target.load(args)
        self.assertEqual(expected, result)

    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    def test__flag_t__multiple_files(self, mock_relpath, mock_isfile):
        args = {
            't':    ['file1', 'file2'],
            'tr':   [],
            'trd':  [],
            'trdo': [],
            'e':    []
        }
        mock_relpath.side_effect = ['./file1', './file2']
        mock_isfile.return_value = True
        expected = ['./file1', './file2']
        result = target.load(args)
        self.assertEqual(expected, result)

    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_t__single_directory(self, mock_walk, mock_relpath, mock_isfile, mock_isdir):
        args = {
            't':    ['dir'],
            'tr':   [],
            'trd':  [],
            'trdo': [],
            'e':    []
        }
        mock_walk.return_value = [
            ('./dir', [], ['file1', 'file2'])
        ]
        mock_relpath.return_value = './dir'
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        expected = ['./dir/file1', './dir/file2']
        result = target.load(args)
        self.assertEqual(expected, result)


class Flag_tr(TestCase):
    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    def test__flag_tr__single_file(self, mock_relpath, mock_isfile):
        args = {
            't':    [],
            'tr':   ['file'],
            'trd':  [],
            'trdo': [],
            'e':    []
        }
        mock_relpath.return_value = './file'
        mock_isfile.return_value = True
        expected = ['./file']
        result = target.load(args)
        self.assertEqual(expected, result)

    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    def test__flag_tr__multiple_files(self, mock_relpath, mock_isfile):
        args = {
            't':    [],
            'tr':   ['file1', 'file2'],
            'trd':  [],
            'trdo': [],
            'e':    []
        }
        mock_relpath.side_effect = ['./file1', './file2']
        mock_isfile.return_value = True
        expected = ['./file1', './file2']
        result = target.load(args)
        self.assertEqual(expected, result)

    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_tr__single_directory(self, mock_walk, mock_relpath, mock_isdir):
        args = {
            't':    [],
            'tr':   ['dir'],
            'trd':  [],
            'trdo': [],
            'e':    []
        }
        mock_walk.return_value = [
            ('./dir', [], ['file0']),
            ('./dir/d', [], ['file1']),
            ('./dir/d/d', [], ['file2'])
        ]
        mock_relpath.return_value = './dir'
        mock_isdir.return_value = True
        expected = ['./dir/file0', './dir/d/file1', './dir/d/d/file2']
        result = target.load(args)
        self.assertEqual(expected, result)

    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_tr__all_files_recursive_in_the_current_directory(self, mock_walk, mock_relpath, mock_isfile, mock_isdir):
        args = {
            't':    [],
            'tr':   ['.'],
            'trd':  [],
            'trdo': [],
            'e':    []
        }
        mock_walk.return_value = [
            ('.', [], ['file0']),
            ('./dir', [], ['file1']),
            ('./dir/d', [], ['file2']),
            ('./dir/d/d', [], ['file3'])
        ]
        mock_relpath.return_value = '.'
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        expected = ['./file0', './dir/file1', './dir/d/file2', './dir/d/d/file3']
        result = target.load(args)
        self.assertEqual(expected, result)


class Flag_trd(TestCase):
    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_trd__single_directory_with_limited_depth(self, mock_walk, mock_relpath, mock_isdir):
        args = {
            't':    [],
            'tr':   [],
            'trd':  [[1, 'dir']],
            'trdo': [],
            'e':    []
        }
        mock_walk.return_value = [
            ('./dir', [], ['file0']),
            ('./dir/d', [], ['file1']),
            ('./dir/d/d', [], ['file2'])
        ]
        mock_relpath.return_value = './dir'
        mock_isdir.return_value = True
        expected = ['./dir/file0', './dir/d/file1']
        result = target.load(args)
        self.assertEqual(expected, result)

    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_trd__single_directory_with_limited_depth_2(self, mock_walk, mock_relpath, mock_isdir):
        args = {
            't':    [],
            'tr':   [],
            'trd':  [[0, 'dir']],
            'trdo': [],
            'e':    []
        }
        mock_walk.return_value = [
            ('./dir', [], ['file0']),
            ('./dir/d', [], ['file1']),
            ('./dir/d/d', [], ['file2'])
        ]
        mock_relpath.return_value = './dir'
        mock_isdir.return_value = True
        expected = ['./dir/file0']
        result = target.load(args)
        self.assertEqual(expected, result)

    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_trd__all_files_recursive_in_the_current_directory(self, mock_walk, mock_relpath, mock_isfile, mock_isdir):
        args = {
            't':    [],
            'tr':   [],
            'trd':  [[2, '.']],
            'trdo': [],
            'e':    []
        }
        mock_walk.return_value = [
            ('.', [], ['file0']),
            ('./dir', [], ['file1']),
            ('./dir/d', [], ['file2']),
            ('./dir/d/d', [], ['file3'])
        ]
        mock_relpath.return_value = '.'
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        expected = ['./file0', './dir/file1', './dir/d/file2']
        result = target.load(args)
        self.assertEqual(expected, result)


class Flag_trdo(TestCase):
    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_trdo__single_directory(self, mock_walk, mock_relpath, mock_isdir):
        args = {
            't':    [],
            'tr':   [],
            'trd':  [],
            'trdo': [[1, 'dir']],
            'e':    []
        }
        mock_walk.return_value = [
            ('./dir', [], ['file0']),
            ('./dir/d', [], ['file1']),
            ('./dir/d/d', [], ['file2'])
        ]
        mock_relpath.return_value = './dir'
        mock_isdir.return_value = True
        expected = ['./dir/d/file1']
        result = target.load(args)
        self.assertEqual(expected, result)


    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_trdo__all_files_recursive_with_selected_depth_1(self, mock_walk, mock_relpath, mock_isfile, mock_isdir):
        args = {
            't':    [],
            'tr':   [],
            'trd':  [],
            'trdo': [[0, '.']],
            'e':    []
        }
        mock_walk.return_value = [
            ('.', [], ['file0']),
            ('./dir', [], ['file1']),
            ('./dir/d', [], ['file2']),
            ('./dir/d/d', [], ['file3'])
        ]
        mock_relpath.return_value = '.'
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        expected = ['./file0']
        result = target.load(args)
        self.assertEqual(expected, result)

    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_trdo__all_files_recursive_with_selected_depth_2(self, mock_walk, mock_relpath, mock_isfile, mock_isdir):
        args = {
            't':    [],
            'tr':   [],
            'trd':  [],
            'trdo': [[3, '.']],
            'e':    []
        }
        mock_walk.return_value = [
            ('.', [], ['file0']),
            ('./dir', [], ['file1']),
            ('./dir/d', [], ['file2']),
            ('./dir/d/d', [], ['file3'])
        ]
        mock_relpath.return_value = '.'
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        expected = ['./dir/d/d/file3']
        result = target.load(args)
        self.assertEqual(expected, result)


class Flag_e(TestCase):
    @mock.patch.object(target.os.path, 'isdir')
    @mock.patch.object(target.os.path, 'isfile')
    @mock.patch.object(target.os.path, 'relpath')
    @mock.patch.object(target.os, 'walk')
    def test__flag_e__all_files_recursive_in_the_current_directory(self, mock_walk, mock_relpath, mock_isfile, mock_isdir):
        args = {
            't':    [],
            'tr':   ['.'],
            'trd':  [],
            'trdo': [],
            'e':    ['2', '3']
        }
        mock_walk.return_value = [
            ('.', [], ['file0']),
            ('./dir', [], ['file1']),
            ('./dir/d', [], ['file2']),
            ('./dir/d/d', [], ['file3'])
        ]
        mock_relpath.return_value = '.'
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        expected = ['./file0', './dir/file1']
        result = target.load(args)
        self.assertEqual(expected, result)
