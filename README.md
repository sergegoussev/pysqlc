<h1>pysqlc</h1>

<p>
<b>pysqlc</b> is an abstraction library for SQL databases (it stands for Python SQL connection). Existing packages, such as <a href="https://pypi.python.org/pypi/mysqlclient">mysqlclient</a> or <a href="https://github.com/mkleehammer/pyodbc">pyodbc</a> require connections and cursors to be made in every script, each time requiring the specification of login information, the host/server, etc. They are also ambigious—leaving the choice of using prepared statements or not up to you. <b>pysqlc</b> simplifies this and allows you to setup your connection once, and then utilize it whenever needed. It also enables easy use of prepared statements. It also faciliates working with multiple databases and makes authentication relatively simple.
</p>

<p>
Compatible with Python 2.7, 3.x (tested with 2.7, 3.5 and 3.6)
</p>


<b>pysqlc</b> is similar (but simpler) than other libraries such as <a href="https://github.com/whiteclover/dbpy">dbpy</a>, and supports:
<ul>
   <li>MySQL;</li>
   <li>SQL Server</li>
   <li>NOTE: Oracle currently not supported by will be included in a later release.</li>
   
</ul>
<hr>

<h4>Installation</h4>
<p>To install, download the repository and install using pip (locally):</p>

    >>> pip install .

<p>or alternatively via git from here directly:</p>

    >>> pip install git+https://github.com/sergegoussev/pysql-con.git

<h4>Quickstart</h4>
<ol>
   <li>Setup and connection:
      <br>
      <p>After installing the <b>pysqlc</b> package, you have an option of how you would like the library to authenticate. The recommended approach is to set up an environmental variable, however you could also authenticate for each connection.</p>
    <p>To follow the environmental variable approach (works the same way as <a href="https://cloud.google.com/deployment-manager/docs/configuration/templates/use-environment-variables">google cloud environmental variables</a>, which points to a json on your computer), create a 'SQL_LOGIN' variable and point it to a .json file somewhere on your computer. You must follow the below structure with the name of the environment you are connecting to, and the various connection requirements.</p>
   
    {
    	"main":{
    		"dbtype":"MySQL",
    		"host":"localhost",
    		"charset":"utf8mb4",
    		"username":"uid",
    		"password":"psw"
    	}
    }
     
        
    <p>The above approach makes it possible for you to specify several environments, just add as needed. Its recommended to set the default environment you will use as "main". If "main" is specified in the json, you do not need to specify the environment every time when connecting. 
    </p>
     
<br>
   <ul>
      <li>NOTE 1: specify either "MySQL" or "SQL Server" under dbtype;</li>
      <li>NOTE 2: "password" section can be ommited. If it is not included, the <b>pysql</b> will ask for the password every time the connection is made (or alternatively look for it to be passed into the DB object upon initiation):</li>
      <ul>
         <li>if password ommited from local variable json and <b>not</b> specified in code:</li>

```python
from pysqlc import DB
db = DB('testdb')
Enter password to login to the database server: #prompt
'pass'
Successfully connected to testdb
```
    
<li>if password ommited from local variable json, but specified in code:</li>

```python
from pysqlc import DB
db = DB('testdb', password='pass')
Successfully connected to testdb
```

<li>if password included in json:</li>

```python
from pysqlc import DB
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
<li>Inserting large list of data: specify 'executemany'=True in the query command and <b>pysql</b> will utilize the <i>cursor.executemany()</i> function:
   
```python
query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
values = [(123,'john smith'),(456,'elon musk'),(789,'bill gates')]
db.query(query, values, q_type='INSERT', executemany=True)
```
</li>
