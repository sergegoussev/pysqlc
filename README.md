[Documentation](https://sergegoussev.github.io/pysqlc/docs/build/html/index.html)

# pysqlc

**pysqlc** is an abstraction library for SQL databases (it stands for Python SQL connection). Existing packages, such as [mysqlclient](https://pypi.python.org/pypi/mysqlclient) or [pyodbc](https://github.com/mkleehammer/pyodbc) require connections and cursors to be made in every script, each time requiring the specification of login information, the host/server, etc. They are also ambigious—leaving the choice of using prepared statements or not up to you. **pysqlc** simplifies this and allows you to setup your connection once, and then utilize it whenever needed. It also enables easy use of prepared statements. Thus it faciliates working with multiple databases and makes authentication relatively simple.

Compatible with Python 2.7, 3.5, 3.6, 3.7

**pysqlc** is similar (but simpler) than other libraries such as [dbpy](https://github.com/whiteclover/dbpy), and supports:
* MySQL;
* SQL Server

## Installation
To install, download the repository and install using pip (locally):

    >>> pip install .

or alternatively via git from here directly:

    >>> pip install git+https://github.com/sergegoussev/pysqlc.git


## Quickstart

To use the library - you first have to connect to your database by initiating the `DB` object, and then write SQL for whatever you are trying to do using `DB.query("")`. That's it! 

When initiating the connection, you can either enter your login info manually, or utilize **pysqlc**'s *environment variable* approach (similar to the approach used by Google APIs). The below example to connect and extract some data from your database assumes you have setup an *environmental variable* for the library to use:
   
```python
from pysqlc import DB

#connect to the database you want
db = DB(env_name="prod", database="database_name", )

#write your SQL query as a string
q = "SELECT * FROM table;"

#and get the data back using one simple function
result = db.query(q)
```

That's it! To read more about how to set up the library and its methods, see [the documentation]( https://sergegoussev.github.io/pysqlc/docs/build/html/index.html)