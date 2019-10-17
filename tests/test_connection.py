import unittest
from pysqlc.connect import DBconnect
import mysql.connector
import os
import json


class TestConnection(unittest.TestCase):

    """
    test various features of a dbconfig() object
    """
    def test_EnvVar(self):
        """
        this test validates whether the 'self.login' var is correctly 
        extracted and coded by the library
        """
        self.env_name = 'prod'
        self.db = DBconnect(env_name=self.env_name)

        with open(os.environ['SQL_LOGIN']) as file:
            j = file.read()
            file.close()
        parsed = json.loads(j)
        login = parsed[self.env_name]
        # if the self.login is equal to the login from here, all is good
        self.assertEqual(login, self.db.login, 'env var good!')

    def test_Conn(self):

        self.env_name = 'prod'
        db = DBconnect(env_name=self.env_name)
        
        # c = self.db.conn.cursor()
        connected_data = db.query("SHOW DATABASES;") #c.execute("SHOW DATABASES;").fetchall()

        login = db.login
        conn = mysql.connector.connect(
            host=login['host'],
            user=login['username'],
            password=login['password'],
            port=login['port'],
            charset=login['charset'],
            database=None,
            auth_plugin='mysql_native_password'
        )

        c2 = conn.cursor()
        separate_data = c2.execute("SHOW DATABASES;").fetchal()
        self.assertEqual(connected_data, separate_data, "connected and data is good")


if __name__ == '__main__':
    print('starting tests...')
    unittest.main()
