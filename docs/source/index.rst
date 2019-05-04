Welcome to pysqlc documentation
===============================

**pysqlc** is an abstraction library for SQL databases (it stands for Python SQL connection). Existing packages, such as `mysqlcient <https://pypi.python.org/pypi/mysqlclient>`_ or `pyodbc <https://github.com/mkleehammer/pyodbc>`_ require connections and cursors to be made in every script, each time requiring the specification of login information, the host/server, etc. They are also ambigious—leaving the choice of using prepared statements or not up to you. **pysqlc** simplifies this and allows you to setup your connection once, and then utilize it whenever needed. It also enables easy use of prepared statements. Thus it faciliates working with multiple databases and makes authentication relatively simple.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README.md
   Reference
   licence

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
