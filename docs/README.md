[HOME](../README.md) | Documentation

# **pysqlc** Documentation

**pysqlc**, works by (1) connecting to a database by name (where it uses the pre-selected connection method), and (2) executes a query on the connected database.

**supported**:
* Python 2.7, 3.x
* MySQL 5.7, 8.0
* SQL Server 2012

**Contents**:
* [Setup](#setup)
    * [Environmental Variable Approach](#environmental-variable-approach)
    * [Specifying environments](#specifying-environments)
* [Methods](#methods)
    * [SELECT](#select)
    * [INSERT](#insert)
    * [UPDATE](#update)
    * [CREATE](#create)
    * [DELETE](#delete)


## Setup

To make connections, there are 2 options:
1. You can set up an environmental variable to not have to pass any login information every time you use the library (*recommended*); or
2. Choose to specify username/password manually for each call

### Environmental Variable Approach
 
To follow the environmental variable approach (works the same way as [google cloud environmental variables](https://cloud.google.com/deployment-manager/docs/configuration/templates/use-environment-variables), which points to a json on your computer), create a 'SQL_LOGIN' variable and point it to a .json file somewhere on your computer. You must follow the below structure with the name of the environment you are connecting to, and the various connection requirements.
   
```json
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
        
You can thus specify several environments, just add as needed. Its recommended to set the default environment you will use as "main" — this way you will not need to specify this environment every time when connecting.
* NOTE 1: specify either "MySQL" or "SQL Server" under dbtype;    	
* NOTE 2: "password" section can be ommited. If it is not included, the **pysqlc** will ask for the password every time the connection is made (or alternatively look for it to be passed into the DB object upon initiation):
    * if password ommited from local variable json and **not** specified in code:

```python
from pysqlc import DB
db = DB('testdb')
Enter password to login to the database server: #prompt
'pass'
Successfully connected to testdb
```
    
if password ommited from local variable json, but specified in code:

```python
from pysqlc import DB
db = DB('testdb', password='pass')
Successfully connected to testdb
```

if password included in json:

```python
from pysqlc import DB
db = DB('testdb')
Successfully connected to testdb
```
#### Specifying environments

If you want to specify the environment type you want to connect to, you can do so using the `env_name` parameter:

```python
from pysqlc import DB
db = DB(db_name='testdb', env_name="dev")
Successfully connected to testdb
```
**NOTE 1**: `env_name` default is set to `'prod'`

**NOTE 2, troubleshooting**: the order of arguments when specifying DB object is `db(db_name="", env_name='prod', ...)`, hence make sure to specify the `env_name` variable as the type of variable you are entering. For example if you specify `db('dev')` for dev environment, **pysqlc** will look for the `dev` database on the `prod` (default) environment

**NOTE 3, dev mode**: **pysqlc** has the ability to print the result of every query statement. If you want to enable it, you can turn it on during initiation:

```python
from pysqlc import DB
db = DB(db_name='testdb', env_name="dev", dev_mode=True)
```

By default, it is turned off. The library will still print out major notifications (errors, DB connections, etc). 

### Manual entry of username and password Approach

**Expand**

# Methods

Once connected to a database, there is  has one main method to call and put all SQL queries into: `db.query(q=query)`. All CRUD methods are supported, they simply require different parameter inputs:

## SELECT

This is the default, hence you do no need to specify anything o

**Input**:
* SQL query to select

**Returns**:
List of tuples

**Example**:

```python
q = "SELECT * FROM table;"
result = db.query(q)
```

## INSERT 

**Input**:
* SQL query to insert 
* data to insert as a list of tuples

**Returns**:
* Nothing

**Example**:

```python
query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
values = [123,'john smith']
db.query(query, values, q_type='INSERT') #q_type='UPDATE' if updating
```

**NOTE**: if you have lots of data to add add, you can specify `'executemany'=True` in the query command and **pysqlc** will utilize the `cursor.executemany()` function:
   
```python
query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
values = [(123,'john smith'),(456,'elon musk'),(789,'bill gates')]
db.query(query, values, q_type='INSERT', executemany=True)
```

## UPDATE 
   
Updating values is much like Inserting data -- you should specify the query and the data, but expect nothing back

**Input**:
* SQL query to update 
* data to update as a list of tuples

**Returns**:
* Nothing

## CREATE
   
Creating a new table (or database, index, etc) does not require anything but the query 

**Input**:
* SQL query to create 

**Returns**:
* Nothing

## DELETE

Deleting is similar to Creating, only the query is required

**Input**:
* SQL query to delete

**Returns**:
* Nothing

# NOTE:

Values should always be passed as a list (even if there is only one value):

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