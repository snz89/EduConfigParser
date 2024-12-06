import unittest

from src.main import (
    delete_comments,
    parse_globals,
    parse_dict,
    dict_to_toml
)

class TestParser(unittest.TestCase):
    def setUp(self):
        self.input = """
        (*
        Multiline
        comment
        *)

        data_base_name := "db_test"
        base_url := "https://github.com/"

        {
            database_config_1 = {
                host = "127.0.0.1";
                port = 5432;
                username = "admin";
                password = "QTYUA3783";
                url = .base_url.;
            }

            database_config_2 = {
                host = "127.0.6.1";
                port = 9999;
                username = "admin";
                password = "QTYUA3783";
                url = .base_url.;
            }
        }
        """
        self.maxDiff = None
    
    def test_delete_comments(self):
        expected = """
        data_base_name := "db_test"
        base_url := "https://github.com/"

        {
            database_config_1 = {
                host = "127.0.0.1";
                port = 5432;
                username = "admin";
                password = "QTYUA3783";
                url = .base_url.;
            }

            database_config_2 = {
                host = "127.0.6.1";
                port = 9999;
                username = "admin";
                password = "QTYUA3783";
                url = .base_url.;
            }
        }
        """
        result = delete_comments(self.input)
        self.assertEqual(expected.strip(), result.strip())
    
    def test_parse_globals(self):
        expected = {
            'data_base_name': 'db_test',
            'base_url': 'https://github.com/'
        }
        result = parse_globals(self.input)
        self.assertEqual(result, expected)
    
    def test_parse_dict(self):
        expected = {
            'database_config_1': {
                'host': '127.0.0.1',
                'port': 5432,
                'username': 'admin',
                'password': 'QTYUA3783',
                'url': 'https://github.com/'
            },
            'database_config_2': {
                'host': '127.0.6.1',
                'port': 9999,
                'username': 'admin',
                'password': 'QTYUA3783',
                'url': 'https://github.com/'
            }
        }
        globals = parse_globals(self.input)
        result = parse_dict(self.input, globals)
        self.assertEqual(result, expected)
    
    def test_dict_to_toml(self):
        expected = """
[database_config_1]
  host = "127.0.0.1"
  port = 5432
  username = "admin"
  password = "QTYUA3783"
  url = "https://github.com/"

[database_config_2]
  host = "127.0.6.1"
  port = 9999
  username = "admin"
  password = "QTYUA3783"
  url = "https://github.com/"
        """
        globals = parse_globals(delete_comments(self.input))
        dict = parse_dict(self.input, globals)
        result = dict_to_toml(dict)
        self.assertEqual(result.strip(), expected.strip())