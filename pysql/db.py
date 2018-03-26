# -*- coding: utf-8 -*-
"""
pysql.db
"""
from __future__ import print_function
from pysql.error import ConnectError, QueryError
import os, json, MySQLdb, pypyodbc
	
class DB:
    '''
    The DB oject creates a connection to the SQL server database, verifies db 
    connection based on db name specified, and executes prepared statemetns. 
    
    Acts as a single interface for I/O to the DB server
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
        if self.dbtype == 'MySQL':
            try:
                self.conn = MySQLdb.connect(host=self.login['host'],
                                            user=self.login['username'],
                                            password=self.password,
                                            db=self.db_name,
                                            charset=self.login['charset'])
            except Exception:
                raise ConnectError("Cannot connect, check login information")
        elif self.dbtype == 'SQL Server':
            try:
                self.conn = pypyodbc.connect(driver='{SQL Server}',
                                             server=self.login['host'],
                                             database=self.db_name,
                                             uid=self.login['username'],
                                             pwd=self.password)
            except Exception:
                raise ConnectError("Cannot connect, check login information")
        else:
            raise ConnectError("Improper database type selected")

    def query(self, sql_query, values=None, q_type="SELECT", executemany=False):
        '''
        This is the function that passes in the query, with 3 options:
            
        If a SELECT query, a result is returned (no extra input necessary)
        If an INSERT query (nothing returned):
            - need q_type = 'INSERT'
            - values - the values that will be committed
            - NOTE: REPLACE works similarly if specified 
        If a CREATE query (nothing returned):
            - need q_type = 'CREATE'
            - values = None (or skip)
        If DELETE query (again, nothing returned):
            - need q_type = 'DELETE'
            - values = None (or skip)
        If UPDATE query (as above)
        If executemany == True -- uses the 'executemany' cursor function

        The error handling is done so as to re-create the cursor in case it 
        expires through lack of use.
        '''
        #cursor error handler:
        try:
            c = self.conn.cursor()
            if executemany is True:
                c.executemany(sql_query, values)
            else:
                c.execute(sql_query, values)
    
        #re-establish the cursor if expired
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            c = self.conn.cursor()
            if executemany is True:
                c.executemany(sql_query, values)
            else:
                c.execute(sql_query, values)

        #return function based on input type
        mod_qs = ('update','insert','replace','delete')
        if q_type == 'INSERT' or q_type == 'REPLACE' or q_type == 'DELETE' or q_type == 'UPDATE':
            if any(q in sql_query.lower() for q in mod_qs):    
                print('{} made'.format(q_type.title()))
                self.conn.commit()
            else:
                raise QueryError('improper q_type used, you are not attempting to make changes but using an alter query type')
        elif q_type is 'SELECT':
            if not any(q in sql_query.lower() for q in mod_qs):
                return c.fetchall()
            else:
                raise QueryError('improper q_type, please do not use SELECT when modifying data')
        
if __name__ == '__main__':
    pass