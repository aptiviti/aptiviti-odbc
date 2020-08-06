import sys
sys.path.append('.')
from aptiviti_odbc import aptiviti_odbc_connection
import unittest
from unittest.mock import Mock, MagicMock
from unittest.mock import patch, call

@patch ('aptiviti_odbc.pyodbc')
@patch ('aptiviti_odbc.pandas')

class TestOdbc(unittest.TestCase):
   def test_connection(self, mock_pandas, mock_pyodbc):
      database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
      self.assertTrue(mock_pyodbc.connect.called)
      self.assertTrue(mock_pyodbc.connect.call_count, 1)
      self.assertEqual(database_connection.connection_string, 'Driver={SQL Server Native Client 11.0};Server=mockhost;UID=mockuser;PWD=mockpassword;database=mockdatabase')
      self.assertEqual(database_connection.BATCH_LIMIT, 1000)
      self.assertEqual(mock_pyodbc.connect.call_args[0][0], database_connection.connection_string)      

   def test_placeholder(self, mock_pandas, mock_pyodbc):
      database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
      self.assertEqual(database_connection.get_placeholder(), '?')

   def test_query(self, mock_pandas, mock_pyodbc):
      database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
      result = database_connection.query('dummy sql')
      self.assertTrue(mock_pandas.read_sql.called)
      self.assertTrue(mock_pandas.read_sql.call_count, 1)
      self.assertEqual(mock_pandas.read_sql.call_args[0][0], 'dummy sql')

   def test_mutate(self, mock_pandas, mock_pyodbc):
      database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
      result = database_connection.mutate('dummy sql')
      self.assertTrue(database_connection.cursor.execute.called, 1)
      self.assertTrue(database_connection.cursor.execute.call_count, 1)
      self.assertEqual(database_connection.cursor.execute.call_args[0][0], 'dummy sql')
      self.assertEqual(len(database_connection.cursor.execute.call_args[0]), 1)
      result = database_connection.mutate('dummy sql', ['mock params'])
      self.assertTrue(database_connection.cursor.execute.called)
      self.assertTrue(database_connection.cursor.execute.call_count, 1)
      self.assertEqual(database_connection.cursor.execute.call_args[0][0], 'dummy sql')
      self.assertEqual(database_connection.cursor.execute.call_args[0][1], ['mock params'])
      self.assertEqual(len(database_connection.cursor.execute.call_args[0]), 2)

   def test_batch_size(self, mock_pandas, mock_pyodbc):
      database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
      batch_size = database_connection.get_batch_size(0, 2, 10, 100)
      self.assertEqual(batch_size, 10)
      batch_size = database_connection.get_batch_size(9, 10, 10, 95)
      self.assertEqual(batch_size, 5)

   def test_get_placeholder_list(self, mock_pandas, mock_pyodbc):
      database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
      placeholder_list = database_connection.get_placeholder_list(10, ['NEWID()'])
      self.assertEqual(placeholder_list, ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?', 'NEWID()'])

   def test_batch_insert(self, mock_pandas, mock_pyodbc):
      database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
      database_connection.batch_insert('dummy sql **values**', [['dummy val']], ['NEWID()'])
      self.assertTrue(database_connection.cursor.execute.called)
      self.assertTrue(database_connection.cursor.execute.call_count, 1)      
      self.assertEqual(database_connection.cursor.execute.call_args[0][0], "dummy sql (?,NEWID())")
      self.assertEqual(database_connection.cursor.execute.call_args[0][1], ['dummy val'])

   def test_batch_query(self, mock_pandas, mock_pyodbc):
      database_connection = aptiviti_odbc_connection('mockhost', 'mockuser', 'mockpassword', 'mockdatabase')
      database_connection.batch_query('dummy sql **values**', ['dummy val'], ['NEWID()'])
      self.assertTrue(mock_pandas.read_sql.called)
      self.assertTrue(mock_pandas.read_sql.call_count, 1)
      self.assertEqual(mock_pandas.read_sql.call_args[0][0], 'dummy sql ?')

if __name__ == '__main__':
   unittest.main()
