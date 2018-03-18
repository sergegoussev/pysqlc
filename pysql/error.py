# -*- coding: utf-8 -*-
"""
pysql.error
"""

class pysqlError(Exception):
    """
    The main exception handler for pysql
    """
    def __init__(self, reason):
        Exception.__init__(self, reason)

class ConnectError(pysqlError):
    """
    Connection error handler
    """
    pass

class QueryError(pysqlError):
    """
    Query error handler
    """
    pass