# -*- coding: utf-8 -*-
"""
pysql.connect
"""
from __future__ import print_function
from pysqlc.error import ConnectError
import os
import json
import mysql.connector
from mysql.connector import errorcode
import pypyodbc
import getpass

class DBconnect:
    
    """
    Base object to connect to a database to be inherited by the pysqlc.DB object
    """

    def __init__(self,
                 env_name="dev",
                 db_name=None,
                 username=None,
                 password=None,
                 host=None,
                 charset=None,
                 port=None,
                 _debug_mode=False):
        '''
        Enter the required information to connect to the SQL server. If environmental
        variable is set, you can skip specifying everything 
        '''
        #set the global variables
        self.host = host
        self.port = port
        self.charset = charset
        self.env_name = env_name
        self.username = username
        self._pass_entered = password
        self.db_name = db_name
        self._debug_mode = _debug_mode
        self.__get_login_info__()
        #if database is specified, connect using the default, else
        #connect to just the DB server
        if db_name is not None:
            try:
                self.connect()
                if self._debug_mode == True:
                    print("Successfully connected to {} database".format(self.db_name))
            except:
                #if a database dame was not specified, provide list of possibles:
                avail_dbs = self.__check_dbs__()
                print('No such database exists, the following are availible:')
                for each in avail_dbs:
                    print(" - {}".format(each[0]))
                print("Please retry with one of the above")
        else:
            self.connect()
            if self._debug_mode == True:
                print("Connected to DB server, no DB was selected")

    def __get_login_info__(self):
        try:
            with open(os.environ['SQL_LOGIN']) as file:
                j = file.read()
                file.close()
            parsed = json.loads(j)
            if self.env_name in parsed:
                self.login = parsed[self.env_name]
            else:
                raise ConnectError(
                    "Improper environment selected, please try again")
            self.dbtype = self.login['dbtype']

        except:
            if (self.host is not None
                and self.charset is not None
                    and self.username is not None):
                self.login = {
                    "host": self.host,
                    "charset": self.charset,
                    "username": self.username
                    
                }
            else:
                raise ConnectError(
                    "No environmental variable detected and server connection information not specified during initialization of the DB object. Please try again")
        if 'password' in self.login:
            self.password = self.login['password']
        elif self.pass_entered is not None:
            self.password = self.pass_entered
        else:
            self.password = getpass.getpass(
                "Enter password to login to the database server: ")

    def __check_dbs__(self):
        q = """
                SELECT 
                	table_schema as `database`
                FROM information_schema.tables 
                
                	WHERE table_schema NOT IN (
                		'information_schema',
                		'performance_schema',
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
                #figure out how to get around the auth_plugin default native psw
                #https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported
                #need to force SSL...
                self.conn = mysql.connector.connect(
                    host=self.login['host'],
                    user=self.login['username'],
                    password=self.password,
                    port=self.port,
                    database=self.db_name,
                    charset=self.charset,
                    #auth_plugin='sha256_password'
                    )
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
            else:
                self.conn.close()
        elif self.dbtype == 'SQL Server':
            try:
                self.conn = pypyodbc.connect(
                    driver='{SQL Server}',
                    server=self.login['host'],
                    database=self.db_name,
                    uid=self.login['username'],
                    pwd=self.password)
            except Exception:
                raise ConnectError("Cannot connect, check login information")
        else:
            raise ConnectError("Improper database type selected")


if __name__ == "__main__":
    pass