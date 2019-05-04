:mod:`pysqlc.DB` --- reference and examples
===========================================

This page contains an overview of **nlpru** and all availible methods

Initiation
----------

.. class:: DB([db_name=""], [env_name="prod"], [username=None], [password=None], [host=None], [charset=None], [dev_mode=False])

    The DB oject creates a connection to the SQL server database, verifies db connection based on db name specified, and executes prepared statements. 

    Acts as a single interface for I/O to the DB server

   :param db_name: name of the database you want to connect to
   :param env_name: environment you wish to connect to, only applicable if you are using the *environmental variable* approach
   :param username: manually input username if not utilizing *environmental variable* approach
   :param password: manually input the passwords if not utilizing *environmental variable* approach
   :param host: specify the server host if not utilizing *environmental variable* approach, for example `"localhost"`
   :param charset: character set if not utilizing *environmental variable* approach, for example `"utf8mb4"`
   :param dev_mode: specify whether you want **pysqlc** to provide transparency on all operations (print to console)

Query
-----

.. method:: DB.query([sql_query], [values=None], [q_type="SELECT"], [executemany=False])

    The main operating method for all CRUD operations. Expects a SQL query as a string, and allows customizations with 3 parameters.

    :param sql_query: mandatory, actual SQL query as a string
    :param values: if `q_type="INSERT"`, the values to go along with the string SQL query. 
    :param q_type: the type of CRUD operation being utilized, `'INSERT'`, `'REPLACE'`, `'DELETE'`, and `'UPDATE'`, and `'CREATE'` are allowed.
    :param executemany: specify if you want to do a batch operation
    :rtype: list of tuples for `q_type="SELECT"`, `None` for all others


Examples
--------

    SELECT query, a result is returned
        - `q_type = "SELECT"` (default)
        - `values` optional

        .. code-block:: python

            q = "SELECT * FROM table;"
            result = db.query(q)

    INSERT query (nothing returned)
        - `q_type = 'INSERT'`
        - `values` - the values that will be committed

        Insert one row

        .. code-block:: python

            query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
            values = [123,'john smith']
            db.query(query, values, q_type='INSERT')

        Insert multiple rows

        .. code-block:: python

            query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
            values = [(123,'john smith'),(456,'elon musk'),(789,'bill gates')]
            db.query(query, values, q_type='INSERT', executemany=True)

    UPDATE query (as above)
        - need q_type = 'DELETE'
        - values = None (or skip)

        .. code-block:: python
        
            query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
            values = [123,'john smith']
            db.query(query, values, q_type='UPDATE')

    REPLACE query (nothing returned)
        - `q_type = 'INSERT'`
        - `values` - the values that will be committed

    CREATE query (nothing returned)
        - need q_type = 'CREATE'
        - values = None (or skip)

    DELETE query (again, nothing returned)
        - need q_type = 'DELETE'
        - values = None (or skip)