<h1>pysql</h1>

<b>pysql</b> is an abstraction library for SQL databases. Existing packages, such as <a href="https://pypi.python.org/pypi/mysqlclient">mysqlclient</a> or <a href="https://github.com/mkleehammer/pyodbc">pyodbc</a> require connections and cursors to be made in every script, each time requiring the specification of login information, the host, etc. They also are ambigious -- leaving the choice of using prepared statements or not up to you. <b>pysql</b> simplifies this and allows you to setup your connection once, and then utilize it whenever needed. 

<b>pysql</b> is similar (but simpler) than other libraries such as <a href="https://github.com/whiteclover/dbpy">dbpy</a>, and supports:
<ul>
   <li>MySQL;</li>
   <li>SQL Server</li>
   <li>NOTE: Oracle currently not supported by will be included in a later release.</li>
   
</ul>
<hr>

<h4>Installation</h4>
<p>To install, download the repository and install using pip (locally):</p>

    >>> pip install .

<h4>Quickstart</h4>
<ol>
   <li>Setup and connection:
      <br>
      <p>After installing the *pysql* package, you must create an environmental variable titled 'SQL_LOGIN' that will store the login information in the local computer, for instance:</p>
   
    {
    	"dbtype":"MySQL", 
    	"host":"localhost",
    	"charset":"utf8mb4",
    	"username":"user",
    	"password":"pass"
    }
<br>
   <ul>
      <li>NOTE 1: specify either "MySQL" or "SQL Server"</li>
      <li>NOTE 2: "password" can be ommited, if it is, the *pysql* will ask for the password every time the connection is made (or alternatively can be passed into the DB object upon initiation):</li>
      <ul>
         <li>if password ommited from local variable json and <b>not</b> specified in code:</li>

```python
from pysql import DB
db = DB('testdb')
Enter password to login to the database server: #prompt
'pass'
Successfully connected to testdb
```
    
<li>if password ommited from local variable json, but specified in code:</li>

```python
from pysql import DB
db = DB('testdb', password='pass')
Successfully connected to testdb
```

<li>if password included in json:</li>
```python
from pysql import DB
db = DB('testdb')
Successfully connected to testdb
```
   </ul>
   </ul>
</li>
    	
<li>Extracting data:
Extraction is super easy once connected to a database:
   
```python
q = "SELECT * FROM table;"
result = db.query(q)
```
</li>

<li>Inserting (or updating) data:
Also very easy, based on prepared statements:

```python
query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
values = (123,'john smith')
db.query(query, values, q_type='INSERT') #q_type='UPDATE' if updating
```

</li>
<li>Inserting large list of data:
   you do not need to specify that you are inserting many records, <b>pysql</b> will automatically recognize it and and <i>cursor.executemany()</i> will be used:
   
```python
query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
values = [(123,'john smith'),(456,'elon musk'),(789,'bill gates')]
db.query(query, values, q_type='INSERT')
```
</li>
</ol>
    
    	
