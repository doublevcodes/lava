from enum import auto, Enum
from typing import Any, Final


class TokenType(Enum):

    IDENT = auto()

    # Data types
    INTEGER = auto()
    POINT = auto()
    STRING = auto()

    # Operators
    EQUAL = auto()
    PLUS = auto()
    DASH = auto()
    STAR = auto()
    SLASH = auto()
    DOUBLE_STAR = auto()
    CARET = auto()
    AT_SYMBOL = auto()
    SINGLE_QUOTE = auto()
    AMPERSAND = auto()
    PIPE = auto()

    # Keywords
    PRINT = auto()

    # To stop linters complaining about accessing private variables
    @property
    def name_(self):
        return self._name_


class Token:
    """Represents a semantic token within Lava source code as determined by the lexer.

    Attributes:
        type_ (TokenType): The type of the token.
        value (Any): The value of the token.
    """

    def __init__(self, type_: TokenType, value: Any = None):
        self.type: Final[TokenType] = type_
        self.value: Final[Any] = value

    def __repr__(self) -> str:
        return f"Token({self.type.name_} with value {self.value})"
