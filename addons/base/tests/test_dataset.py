# -*- coding: utf-8 -*-
import mock
import unittest2
import base.controllers.main

class TestDataSetController(unittest2.TestCase):
    def setUp(self):
        self.dataset = base.controllers.main.DataSet()
        self.request = mock.Mock()
        self.read = self.request.session.model().read
        self.search = self.request.session.model().search

    def test_empty_find(self):
        self.search.return_value = []
        self.read.return_value = []

        self.assertFalse(self.dataset.do_find(self.request, 'fake.model'))
        self.read.assert_called_once_with([], False)

    def test_regular_find(self):
        self.search.return_value = [1, 2, 3]

        self.dataset.do_find(self.request, 'fake.model')
        self.read.assert_called_once_with([1, 2, 3], False)

    def test_ids_shortcut(self):
        self.search.return_value = [1, 2, 3]
        self.read.return_value = [
            {'id': 1, 'name': 'foo'},
            {'id': 2, 'name': 'bar'},
            {'id': 3, 'name': 'qux'}
        ]

        self.assertEqual(
            self.dataset.do_find(self.request, 'fake.model', ['id']),
            [{'id': 1}, {'id': 2}, {'id': 3}])
        self.assertFalse(self.read.called)
