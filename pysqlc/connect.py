from __future__ import print_function
from pysqlc.error import ConnectError, EnvVariableError, DataInputError
import json
import os
import mysql.connector
import pypyodbc
import getpass

class DBconnect:

    def __init__(
            self, 
            env_name="prod",
            _debug_mode=False,
            **kwargs):
        """
        Enter the required information to connect to the SQL server. If environmental
        variable is set up, no manual configuration of the login info is required, else it is expected

        @param:
            - env_name = "dev" (default) - specify the dbms environment to connect to
            - _debug_mode = False (default) - specify if you want to print indicators throughout the connection
        *kwargs - if you elect not to use the environmental variable approach, enter the login variables manually:
            - dbtype - 'MySQL' and 'SQL Server' supported
            - username - specify the username
            - password - specify the password
                NOTE: if you wish to not type your password in manually (avoid echoing), you can omit it and the library will 
                ask you to specify it later using the python getpass() method.  
            - host - enter the ip of the server host, for instance 'localhost'
            - charset - enter the charset
            - port - enter the port
        """
        self.env_name = env_name
        self._debug_mode = _debug_mode
        # self.__setup_with_env_variable__()
        try:
            # attempt the environmental variable approach
            if self._debug_mode == True:
                print("Setting access variable with data from env variable")
            self.__setup_with_env_variable__()
        except EnvVariableError:
            # if the env variable approach errors out, attempt manual
            if self._debug_mode == True:
                print("Setting access variable with data manually")
            self.__setup_manually__(**kwargs)
        except Exception as e:
            #if unexpected error from above 2 methods is raised, then specify that unknown error occured
            raise DataInputError(
                "Error setting up connection variables: {}".format(e))
        finally:
            #once self.login set up, try connecting to the dbms
            try:
                if self._debug_mode == True:
                    print("Login info cashed, now trying connecting")
                #if no database is chosen, then set it as None
                if "database" in kwargs:
                    if self._debug_mode == True:
                        print("Connecting to DBMS & a specific DB")
                    self.login['database'] = kwargs['database']
                else:
                    if self._debug_mode == True:
                        print("Connecting only to DBMS, not to a specific DB")
                    self.login['database'] = None
                #now actually try to connect
                if self._debug_mode == True:
                    print("Initiating the connection")
                self.connect()
            except Exception as e:
                raise ConnectError("Invalid info to conenct: {}".format(e))

    #-------supporting methods for __init__() ---------------------------------------------


    def __setup_with_env_variable__(self):
        """
        Attempt to find the 'SQL_LOGIN' env variable and setup the 
        master function in memory to connect to
        """
        try:
            with open(os.environ['SQL_LOGIN']) as file:
                j = file.read()
                file.close()
            parsed = json.loads(j)
            if self.env_name in parsed:
                self.login = parsed[self.env_name]
                if 'password' not in self.login:
                    self.__enter_password_manually__()
            else:
                raise ConnectError(
                    "{} db environment not found in environmental variable".format(self.env_name))
        except:
            raise EnvVariableError("No environmental variable found")

    def __setup_manually__(self, **kwargs):
        """
        If the environmental variable failed, setup manual approach using 
        specified **args
        """
        self.login = {}
        for key, value in kwargs.items():
            if key in ("dbtype", "username", "password", "host", "charset", "port"):
                self.login[key] = value
            else:
                raise DataInputError("{k} unexpected parameter".format(k=key))
        if "password" not in self.login:
            self.__enter_password_manually__()

    def __enter_password_manually__(self):
        """
        For both automatic and manual -- if the password was not specified, allow the user to enter it manually
        """
        self.login['password'] = getpass.getpass(
            "Enter password to login to the database server: ")

    def connect(self):
        """
        Method connecting to the DMBS server based on specified values
        """
        if self.login['dbtype'] == "MySQL":
            if self._debug_mode == True:
                print("...conecting to a MySQL server DB...")
            # figure out how to get around the auth_plugin default native psw
            # https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported
            # need to force SSL...
            self.conn = mysql.connector.connect(
                host=self.login['host'],
                user=self.login['username'],
                password=self.login['password'],
                port=self.login['port'],
                charset=self.login['charset'],
                database=self.login['databaseac'],
                auth_plugin='mysql_native_password'
            )
            if self._debug_mode == True:
                print("...connection made...")
        elif self.login['dbtype'] == "SQL Server":
            self.conn = pypyodbc.connect(
                driver="{SQL Server}",
                server=self.login['host'],
                database=self.login['database'],
                port=self.login['port'],
                uid=self.login['username'],
                psw=self.login['password']
            )
        else:
            raise ConnectError(
                "{} db type is not supported".format(self.login['dbtype']))

    # def __test__connection__(self):
    #     c = self.conn.cursor()

    #     c.execute("SHOW DATABASES;")
    #     for db in c.fetchall():
    #         print(db)


if __name__ == "__main__":
    co = DBconnect()
    # co.__test__connection__()
    # co.connect()

    # login = co.login
    # print(login)

    # conn = mysql.connector.connect(
    #     host=login['host'],
    #     user=login['username'],
    #     password=login['password'],
    #     port=login['port'],
    #     charset=login['charset'],
    #     database=None,
    #     auth_plugin='mysql_native_password'
    # )

    # c = conn.cursor()

    # c.execute("SHOW DATABASES;")
    # for db in c.fetchall():
    #     print(db)
