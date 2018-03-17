#pysql

*pysql* is an abstraction library for SQL databases. Existing packages, such as mysqlclient or pyodbc require connections and cursors to be made in every script, each time requiring the specification of login information, the host, etc. They also are ambigious -- leaving the choice of using prepared statements or not up to you. *pysql* simplifies this and allows you to setup your connection once, and then utilize it whenever needed. 

*pysql* is similar (but simpler) than other libraries such as <a href="https://github.com/whiteclover/dbpy">dbpy</a>, and supports:
    * MySQL;
    * SQL Server;
    * NOTE: can be expanded to support Oracle, but not included in current version.
<hr>

To install, download the repository and install using pip (locally):
    >>> pip install .

##Quickstart:
###(1) Setup and connection:
After installing the *pysql* package, you must create an environmental variable titled 'SQL_LOGIN' that will store the login information in the local computer, for instance:
    {
    	"dbtype":"MySQL", 
    	"host":"localhost",
    	"charset":"utf8mb4",
    	"username":"user",
    	"password":"pass"
    }
    - NOTE 1: specify either "MySQL" or "SQL Server"
    - NOTE 2: "password" can be ommited, if it is, the *pysql* will ask for the password every time the connection is made (or alternatively can be passed into the DB object upon initiation):
        - if no password specified:
    	>>> from pysql import DB
    	>>> db = DB('testdb')
    	>>> Enter password to login to the database server: 'pass'
    	>>> Successfully connected to testdb
    
        - if password specified:
    	>>> from pysql import DB
    	>>> db = DB('testdb', password='pass')
    	>>> Successfully connected to testdb
    	
###(2) Extracting data:
Extraction is super easy once connected to a database:
    >>> q = "SELECT * FROM table;"
    >>> result = db.query(q)

###(3) Inserting data:
Also very easy, based on prepared statements:
    >>> query = "INSERT IGNORE INTO table (userid, username) VALUES (%s, %s);"
    >>> values = (123,'john smith')
    >>> db.query(query, values, q_type='INSERT')

    
    	