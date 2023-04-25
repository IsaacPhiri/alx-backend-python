#!/usr/bin/env python3
"""
utils_test
"""


import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict, Callable
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, MagicMock


class TestAccessNestedMap(unittest.TestCase):
    pass

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_output):
        self.assertEqual(access_nested_map(nested_map, path), expected_output)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: \
            Mapping, path: Sequence):
        """Tests that a KeyError is raised for certain inputs"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(context.exception.args[0], path[-1])

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        with patch('requests.get') as mock_get:
            mock_json = MagicMock(return_value=test_payload)
            mock_get.return_value = MagicMock(json=mock_json)

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):

    def test_memoize(self):

        class TestClass:

            def __init__(self):
                self.calls = 0

            def a_method(self):
                self.calls += 1
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            mock_a_method.assert_called_once()
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
