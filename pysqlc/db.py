# -*- coding: utf-8 -*-
"""
pysql.db
"""
from __future__ import print_function
from pysqlc.error import QueryError
from pysqlc.connect import DBconnect
from mysql.connector.errors import Error

class DB(DBconnect):
    '''
    The DB oject creates a connection to the SQL server database, verifies db 
    connection based on db name specified, and executes prepared statements. 

    Acts as a single interface for I/O to the DB server
    '''
    def query(self, sql_query, values=None, q_type="SELECT", executemany=False):
        '''
        The main operating method for all CRUD operations. Expects a SQL query 
        as a string, and allows customizations with 3 parameters.

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
        '''
        # cursor error handler:
        try:
            c = self.conn.cursor()
            if executemany is True:
                c.executemany(sql_query, values)
            else:
                c.execute(sql_query, values)

        # re-establish the cursor if expired
        #https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html
        except (Error):
            #(errno=2006) meant to be "MySQL server has gone away"
            self.connect()
            c = self.conn.cursor()
            if executemany is True:
                c.executemany(sql_query, values)
            else:
                c.execute(sql_query, values)

        # return function based on input type
        mod_qs = ('update ', 'insert ', 'replace ', 'delete ', 'create ')
        if q_type == 'INSERT' or q_type == 'REPLACE' or q_type == 'DELETE' or q_type == 'UPDATE' or q_type == 'CREATE':
            if any(q in sql_query.lower() for q in mod_qs):
                if self._debug_mode == True:
                    print('{} made'.format(q_type.title()))
                self.conn.commit()
            else:
                raise QueryError(
                    'improper q_type used, you are not attempting to make changes but using an alter query type')
        elif q_type is 'SELECT':
            if not any(q in sql_query.lower() for q in mod_qs):
                return list(c.fetchall())
            else:
                raise QueryError(
                    'improper q_type, please do not use SELECT when modifying data')


if __name__ == '__main__':
    db = DB('dev')
