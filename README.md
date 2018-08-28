HOME | [Documentation](docs/README.md)

# pysqlc

**pysqlc** is an abstraction library for SQL databases (it stands for Python SQL connection). Existing packages, such as [mysqlclient](https://pypi.python.org/pypi/mysqlclient) or [pyodbc](https://github.com/mkleehammer/pyodbc) require connections and cursors to be made in every script, each time requiring the specification of login information, the host/server, etc. They are also ambigious—leaving the choice of using prepared statements or not up to you. **pysqlc** simplifies this and allows you to setup your connection once, and then utilize it whenever needed. It also enables easy use of prepared statements. Thus it faciliates working with multiple databases and makes authentication relatively simple.

Compatible with Python 2.7, 3.5, 3.6

**pysqlc** is similar (but simpler) than other libraries such as [dbpy](https://github.com/whiteclover/dbpy), and supports:
* MySQL;
* SQL Server

NOTE: Oracle currently not supported by will be included in a later release.

## Installation
To install, download the repository and install using pip (locally):

    >>> pip install .

or alternatively via git from here directly:

    >>> pip install git+https://github.com/sergegoussev/pysqlc.git


## Quickstart

Make sure you read how to [set up the library](docs/README.md#setup), as you can make use much easier by using the *environment variable* approach 

Lets say you want to connect to a database and extract some data:
   
```python
from pysqlc import DB

#connect to the database you want
db = DB('testdb')

#write your SQL query as a string
q = "SELECT * FROM table;"

#and get the data back using one simple function
result = db.query(q)
```

That's it! To read more about how to set up the library and its methods, see [the documentation](docs/README.md)