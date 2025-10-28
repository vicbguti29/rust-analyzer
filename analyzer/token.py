from dataclasses import dataclass


@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int
    # Opcional: literal, end_line, end_column
    literal: object = None
    end_line: int = None
    end_column: int = None
