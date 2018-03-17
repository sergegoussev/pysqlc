# -*- coding: utf-8 -*-
"""
pysql.connection
"""

from pysql.error import ConnectError
import os, json, MySQLdb, pyodbc

class Connection:
    '''
    The pysql connection object establishes and re-authenticates the connection 
    as necessary
    '''
    def __init__(self, db_name="", password=None):
        self.pass_entered = password
        self.db_name = db_name
        self.__get_login_info__()
        if db_name is not "":
            try:
                self.connect()
                print("Successfully connected to {} database".format(self.db_name))
            except:
                self.db_name = ""
                self.connect()
                print('No such database exists, the following are availible:')
                for each in self.__check_dbs__():
                    print(" - {}".format(each[0]))
                print("Please retry with one of the above")
        else:
            print("No DB selected, please select one of the following databases and try again")
            self.connect()
            for each in self.__check_dbs__():
                print(" - {}".format(each[0]))
    
    def __get_login_info__(self):
        j = open(os.environ['SQL_LOGIN']).read()
        self.login = json.loads(j)
        self.dbtype = self.login['dbtype']
        if 'password' in self.login:
            self.password = self.login['password']
        elif self.pass_entered is not None:
            self.password = self.pass_entered
        else:
            self.password = input("Enter password to login to the database server: ")
            
    def __check_dbs__(self):
        q = """
                SELECT 
                	table_schema as `database`
                FROM information_schema.tables 
                
                	WHERE engine='InnoDB'
                	AND table_schema NOT IN (
                		'information_schema',
                		'sys',
                		'mysql'
                        )
                
                	GROUP BY `database`
                	ORDER BY `database` ASC;
                """
        return self.query(q)

    def connect(self):
        if self.dbtype is 'MySQL':
            try:
                self.conn = MySQLdb.connect(host=self.login['host'],
                    user=self.login['username'],
                    password=self.password,
                    db=self.db_name,
                    charset=self.login['charset'])
            except Exception:
                raise ConnectError("Cannot connect, check login information")
        if self.dbtype is 'SQL Server':
            try:
                self.conn = pyodbc.connect(host=self.login['host'],
                    user=self.login['username'],
                    password=self.password,
                    db=self.db_name,
                    charset=self.login['charset'])
            except Exception:
                raise ConnectError("Cannot connect, check login information")
                
if __name__ == '__main__':
    pass