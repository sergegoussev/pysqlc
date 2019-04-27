# -*- coding: utf-8 -*-
"""
pysql.error
"""


class pysqlcError(Exception):
    """
    The main exception handler for pysql
    """

    def __init__(self, reason):
        Exception.__init__(self, reason)


class ConnectError(pysqlcError):
    """
    Connection error handler
    """
    pass


class QueryError(pysqlcError):
    """
    Query error handler
    """
    pass
