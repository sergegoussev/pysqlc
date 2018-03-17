# -*- coding: utf-8 -*-
"""
pysql.db
"""
import MySQLdb
from pysql.connection import Connection
	
class DB(Connection):
    '''
    The DB oject creates a connection to the SQL server database, verifies db 
    connection based on db name specified, and executes prepared statemetns. 
    
    Acts as a single interface for I/O to the DB server
    '''

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
    
        #suppress the duplicate entry error (but not others)
        except MySQLdb.IntegrityError as e:
            if e.args[0] == 1062:
                pass
            else:
                raise e
                
        #re-establish the cursor if expired
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            c = self.conn.cursor()
            if executemany is True:
                c.executemany(sql_query, values)
            else:
                c.execute(sql_query, values)

        #return function based on input type
        if q_type is 'INSERT' or q_type is 'REPLACE':
            self.conn.commit()
        if q_type is 'SELECT':
            return c.fetchall()
        
if __name__ == '__main__':
    pass
