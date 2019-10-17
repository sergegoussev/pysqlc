# Introduction and Setup

**pysqlc**, works by (1) connecting to a database of your choice, and (2) executing a `SQL` query on it. Authentication, utilization of cursors (and other SQL things) are done for you. 

**supported**:
* Python 2.7, 3.x
* MySQL 5.7, 8.0
* SQL Server 2012, 2016

## Installation
At this point, **pysqlc** is not hosted on PyPI, so to install the library you need to download it from github. There are two ways you can do this, you can go to its [github repo](https://github.com/sergegoussev/pysqlc), download it/clone it locally, and install using using pip (locally):

    >>> pip install .

or alternatively via pip and git directly:

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

## Ways to authenticate

To make connections, there are 2 options:
1. You can set up an *environmental variable* to not have to pass any login information every time you use the library (*recommended*); or
2. Choose to specify username/password manually.
 
To follow the environmental variable approach (works the same way as [google cloud environmental variables](https://cloud.google.com/deployment-manager/docs/configuration/templates/use-environment-variables), which points to a json on your computer), create a 'SQL_LOGIN' variable on your PC and point it to a .json file somewhere on your computer. The JSON file must follow the below structure with the name of the environment you are connecting to, and the various connection requirements:
   
```python
    {
    	"prod":{
    		"dbtype":"MySQL",
    		"host":"localhost",
    		"charset":"utf8mb4",
    		"username":"uid",
    		"password":"psw"
    	}
    }
```
        
You can specify several environments, just add others as needed. Its recommended to set the default environment you will use as "prod" — this way you will not need to specify this environment every time when connecting.
* specify either "MySQL" or "SQL Server" under dbtype;    	
* "password" section can be ommited. If it is not included, the **pysqlc** will ask for the password every time the connection is made (or alternatively look for it to be passed into the DB object upon initiation):

    **Examples**:

    If password ommited from local variable json and **not** specified in code:

    ```python
    from pysqlc import DB
    db = DB(database='testdb')
    Enter password to login to the database server: #prompt
    '****'
    Successfully connected to testdb
    ```
    
    If password ommited from local variable json, but specified in code:

    ```python
    from pysqlc import DB
    db = DB(database='testdb', password='pass')
    Successfully connected to testdb
    ```

    If password included in json:

    ```python
    from pysqlc import DB
    db = DB(database='testdb')
    Successfully connected to testdb
    ```

## Custom Configuration

### Specifying environments

If you have setup your `JSON` file to point towards multiple environments, you can specify the environment of interest upon initating the `DB()` object by utilizing the `env_name` parameter:

```python
from pysqlc import DB
db = DB(env_name="dev", database='testdb')
Successfully connected to testdb
```

By default, `env_name` is set to `'prod'`

**Troubleshooting**

The order of arguments when specifying DB object is `db(database="", env_name='prod', ...)`, hence make sure to specify the `env_name` variable as the type of variable you are entering. For example if you specify `db('dev')` for dev environment, **pysqlc** will look for the `dev` database on the `prod` (default) environment

### Dev mode

**pysqlc** has the ability to print the result of every query statement to give you more visibility of what is going on. If you want to enable it, you can turn it on during initiation:

```python
from pysqlc import DB
db = DB(env_name="dev", database='testdb', dev_mode=True)
```

By default, `dev_mode=False`. The library will still print out major notifications (errors, DB connections, etc).

### Note on `values` input

When inputting data into the `values` parameter, always passed in as a list (even if there is only one value):

```python
q1 = "REPLACE INTO table (name) VALUES (%s);"
db.query(query=q1, values=['John Smith'], q_type='REPLACE')

#or multiple data values:
q2 = """
    UPDATE table
    SET number=%s
    WHERE userid='%s';
    """
db.query(query=q2, values=[123, 'john-123'], q_type="UPDATE")
```