"""Drolta Query Engine."""

from __future__ import annotations

import logging
import sqlite3

from drolta.ast import generate_ast
from drolta.data import EngineData
from drolta.interpreter import DroltaResult, Interpreter, InterpreterMode

_logger = logging.getLogger(__name__)


class QueryEngine:
    """
    A QueryEngine manages user-defined content and handles queries to SQLite.

    Parameters
    ----------
    db : sqlite3.Connection
        A SQlite database Connection.
    """

    __slots__ = ("_db", "_data", "_interpreter")

    _db: sqlite3.Connection
    _data: EngineData
    _interpreter: Interpreter

    def __init__(self, db: sqlite3.Connection) -> None:
        self._db = db
        self._data = EngineData()
        self._interpreter = Interpreter(self._db, self._data)

    def execute_script(self, drolta_script: str) -> None:
        """Load rules and aliases from a Drolta script.

        Parameters
        ----------
        drolta_script : str
            Drolta script text containing rule and alias definitions.
        """

        _logger.debug("Generating drolta AST.")

        drolta_ast = generate_ast(drolta_script)

        _logger.debug("Executing drolta script.")

        self._interpreter.mode = InterpreterMode.SCRIPT_EVAL
        self._interpreter.visit(drolta_ast)

        return

    def execute(self, drolta_query: str) -> DroltaResult:
        """Query the SQLite database and return a cursor to the results.

        Parameters
        ----------
        drolta_query : str
            Text defining a Drolta query.
        """

        _logger.debug("Generating drolta AST.")

        drolta_ast = generate_ast(drolta_query)

        _logger.debug("Executing drolta query.")

        self._interpreter.mode = InterpreterMode.QUERY_EVAL
        self._interpreter.visit(drolta_ast)

        return self._interpreter.result
