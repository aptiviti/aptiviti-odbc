import sys
sys.path.append('.')
from aptiviti_odbc import aptiviti_odbc_connection
import unittest
from unittest.mock import Mock, MagicMock
from unittest.mock import patch, call

@patch ('aptiviti_odbc.pyodbc')

class TestOdbc(unittest.TestCase):
    def test_connection(self, mock_pyodbc):
       database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
       self.assertTrue(mock_pyodbc.connect.called)
       self.assertTrue(mock_pyodbc.connect.call_count, 1)
       self.assertEqual(database_connection.connection_string, 'Driver={SQL Server Native Client 11.0};Server=mockhost;UID=mockuser;PWD=mockpassword;database=mockdatabase')
       self.assertEqual(database_connection.BATCH_LIMIT, 1000)
       self.assertEqual(mock_pyodbc.connect.call_args[0][0], database_connection.connection_string)

if __name__ == '__main__':
   unittest.main()
