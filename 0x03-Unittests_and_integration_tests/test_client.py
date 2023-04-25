#!/usr/bin/env python3
"""
Test Client
"""


import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from unittest import TestCase
from parameterized import parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": True})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json, expected_payload):
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        assert GithubOrgClient.has_license(repo, license_key) == expected
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected_result)

    @patch("client.get_json")
    def test_public_repos_url(self, mock_get_json):
        mock_get_json.return_value = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/google/repos")

    @mock.patch('client.GithubOrgClient._public_repos_url', new_callable=mock.PropertyMock)
    def test_public_repos_url(self, mock_property):
        """Test _public_repos_url method"""
        org_name = 'test_org'
        expected = f'https://api.github.com/orgs/{org_name}/repos'
        mock_property.return_value = expected
        g = GithubOrgClient(org_name)
        assert g._public_repos_url == expected

    @mock.patch('requests.get')
    @mock.patch('client.GithubOrgClient._public_repos_url', new_callable=mock.PropertyMock)
    def test_public_repos(self, mock_property, mock_get):
        """Test public_repos method"""
        repo1 = {'name': 'test_repo1', 'license': {'key': 'my_license'}}
        repo2 = {'name': 'test_repo2', 'license': {'key': 'other_license'}}
        mock_get.return_value.json.return_value = [repo1, repo2]
        mock_property.return_value = 'http://testurl.com/repos'
        g = GithubOrgClient('test_org')
        repos = g.public_repos('my_license')
        assert repos == ['test_repo1']
        mock_get.assert_called_once_with('http://testurl.com/repos')
        mock_property.assert_called_once()

@parameterized_class("payload", [org_payload])
class TestIntegrationGithubOrgClient(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.get_json")
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        self.mock_get.side_effect = [
            self.payload,
            repos_payload,
        ]
        client = GithubOrgClient("some-org")
        self.assertEqual(client.public_repos(), expected_repos)

    def test_public_repos_with_license(self):
        self.mock_get.side_effect = [
            self.payload,
            repos_payload,
        ]
        client = GithubOrgClient("some-org")
        self.assertEqual(client.public_repos(license="apache-2.0"), apache2_repos)
